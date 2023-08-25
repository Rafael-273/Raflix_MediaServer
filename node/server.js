const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

const server = http.createServer((request, response) => {
  const videoUrl = request.url;
  const videoPath = url.parse(videoUrl).pathname.slice(1); // Remove o primeiro caractere ("/") da URL

  const projectDirectory = path.dirname(__dirname);
  const filePath = path.join(projectDirectory, videoPath);

  if (!fs.existsSync(filePath)) {
    response.writeHead(404, { 'Content-Type': 'text/plain' });
    response.end('Vídeo não encontrado');
    return;
  }

  const stat = fs.statSync(filePath);

  // Obtenha a extensão do arquivo para definir o Content-Type corretamente
  const fileExtension = path.extname(filePath).toLowerCase();
  let contentType = 'video/mp4'; // Defina um valor padrão para outros formatos de vídeo

  if (fileExtension === '.mp4') {
    contentType = 'video/mp4';
  } else if (fileExtension === '.webm') {
    contentType = 'video/webm';
  } else if (fileExtension === '.mkv') {
    contentType = 'video/x-matroska';
  }

  response.setHeader('Cache-Control', 'public, max-age=3600');

  response.writeHead(200, {
    'Content-Type': contentType,
    'Content-Length': stat.size
  });

  const readStream = fs.createReadStream(filePath);
  readStream.pipe(response);
});

const port = 3000;
server.listen(port, 'localhost', () => {
  console.log(`Servidor Node.js executando em http://localhost:${port}`);
});
