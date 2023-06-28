const express = require('express');
const router = express.Router();
const path = require('path');
const url = require('url');

router.get('/:videoPath', (req, res) => {
  const videoPath = req.params.videoPath;
  const filePath = path.join('/home/rafael/Música/Raflix_MediaServer/Raflix_MediaServer', videoPath);

  // Aqui você pode adicionar a lógica para verificar se o arquivo existe e tratar os erros, se necessário.

  // Envie o arquivo de vídeo como resposta
  res.setHeader('Content-Type', 'video/mp4');
  res.sendFile(filePath);
});

module.exports = router;