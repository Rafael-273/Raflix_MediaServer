const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');
const express = require('express');

const app = express();

function stream_response(res, file_path, content_type) {
  const readStream = fs.createReadStream(file_path);

  readStream.on('data', function(data) {
    const flushed = res.write(data);
    // Pause the read stream when the write stream gets saturated
    if (!flushed)
      readStream.pause();
  });

  res.on('drain', function() {
    // Resume the read stream when the write stream gets hungry
    readStream.resume();
  });

  readStream.on('end', function() {
    res.end();
  });

  readStream.on('error', function(err) {
    console.error('Exception', err, 'while streaming', file_path);
    res.end();
  });
}

app.get('/skip-video', (req, res) => {
  const videoPath = 'caminho/do/seu/video.mp4'; // Substitua pelo caminho do seu vídeo
  const seconds = parseInt(req.query.seconds, 10);

  const ffmpeg = spawn('ffmpeg', [
    '-i',
    videoPath,
    '-ss',
    seconds.toString(),
    '-c',
    'copy',
    'output.mp4'
  ]);

  ffmpeg.on('exit', (code) => {
    if (code === 0) {
      // Vídeo processado com sucesso
      res.sendStatus(200);
    } else {
      // Ocorreu um erro durante o processamento do vídeo
      res.sendStatus(500);
    }
  });
});


http
  .createServer(function(request, response) {
    const videoUrl = request.url;
    const videoPath = url.parse(videoUrl).pathname.slice(1); // Remove o primeiro caractere ("/") da URL

    const filePath = path.join('/home/rafael/Documentos/Raflix/Raflix_MediaServer', videoPath);

    if (!fs.existsSync(filePath)) {
      response.writeHead(404, { 'Content-Type': 'text/plain' });
      response.end('Vídeo não encontrado');
      return;
    }

    const stat = fs.statSync(filePath);

    response.writeHead(200, {
      'Content-Type': 'video/mp4',
      'Content-Length': stat.size
    });

    stream_response(response, filePath, 'video/mp4');
  })
  .listen(3000, 'localhost');

console.log('Servidor Node.js executando em http://localhost:3000');
