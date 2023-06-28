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

  response.setHeader('Cache-Control', 'public, max-age=3600');

  response.writeHead(200, {
    'Content-Type': 'video/mp4',
    'Content-Length': stat.size
  });

  const readStream = fs.createReadStream(filePath);
  readStream.pipe(response);
});

const port = 3000;
server.listen(port, 'localhost', () => {
  console.log(`Servidor Node.js executando em http://localhost:${port}`);
});