    //
    
    var player = videojs('my-video');
    let lastTime = 0;

    videojs('my-video', {}, function() {
      var player = this;
      player.controlBar.removeChild('PlayToggle');
      player.controlBar.removeChild('CurrentTimeDisplay');
      player.controlBar.removeChild
    })

    //play and pause

    var playButton = document.querySelector('.play_pause');
    var iconPausePlay = document.querySelector('.pause-play')
    playButton.addEventListener('click', function() {
      if (player.paused()) {
        player.play();
        iconPausePlay.innerHTML = "play_arrow";
      } else {
        player.pause();
        iconPausePlay.innerHTML = "pause";
      }
    });

    // Play e Pause na Tela

    player.on('click', function() {
        if (this.paused()) {
          this.play();
          iconPausePlay.innerHTML = "play_arrow";
        } else {
          this.pause();
          iconPausePlay.innerHTML = "pause";
        }
      });

    // Play e Pause com a tecla espaço

    document.addEventListener('keydown', function(event) {
      if (event.code === 'Space') {
        event.preventDefault();
        var player = videojs('my-video');
        if (player.paused()) {
          player.play();
          iconPausePlay.innerHTML = "play_arrow";
        } else {
          player.pause();
          iconPausePlay.innerHTML = "pause";
        }
      }
    });    

    // Retroceder em 10 segundos

    document.querySelector('.rewind').addEventListener('click', function() {
        var videoPlayer = videojs('my-video');
        videoPlayer.currentTime(videoPlayer.currentTime() - 10);
    });

    // Avançar em 10 segundos

    // document.querySelector('.fast-forward').addEventListener('click', function() {
    //     var videoPlayer = videojs('my-video');
    //     videoPlayer.currentTime(videoPlayer.currentTime() + 10);
    // });

    function skipVideo(seconds) {
      // Faz uma solicitação ao servidor Node.js para avançar o vídeo
      fetch('/skip-video?seconds=' + seconds)
        .then(response => {
          // Verifica se a solicitação foi bem-sucedida
          if (response.ok) {
            console.log('Vídeo avançado em ' + seconds + ' segundos');
          } else {
            console.error('Falha ao avançar o vídeo');
          }
        })
        .catch(error => {
          console.error('Erro na solicitação', error);
        });
    }
    

    // Volume

    const volumeControl = document.querySelector(".volume_range");

    volumeControl.addEventListener("input", () => {
        const volumeValue = volumeControl.value / 100; // Converter o valor para um decimal entre 0 e 1
        player.volume(volumeValue);
    });

    //Picture in Picture

    const pipButton = document.querySelector(".picture-in-picture");

    pipButton.addEventListener("click", function() {
      if (document.pictureInPictureElement === player) {
        document.exitPictureInPicture();
      } else {
        player.requestPictureInPicture();
      }
    });

    // Fullscreen

    const fullScreenButton = document.querySelector(".full-screen");

    fullScreenButton.addEventListener("click", () => {
    if (player.requestFullscreen) {
        player.requestFullscreen();
    } else if (player.msRequestFullscreen) {
        player.msRequestFullscreen();
    } else if (player.mozRequestFullScreen) {
        player.mozRequestFullScreen();
    } else if (player.webkitRequestFullscreen) {
        player.webkitRequestFullscreen();
    }
    });

    // Fullscreen com doubleclick

    const video = document.querySelector('video');

    video.addEventListener('dblclick', () => {
        if (document.fullscreenElement) {
            document.exitFullscreen();
          }
        else {
            video.requestFullscreen();
        }
    });


    // Contador 

    player.on('timeupdate', function() {
      const currentTime = this.currentTime();
      const duration = this.duration();

      const currentTimeFormatted = formatTime(currentTime);
      const durationFormatted = formatTime(duration);

      const currentTimeElem = document.querySelector('.current-time');
      const durationElem = document.querySelector('.duration');

      currentTimeElem.textContent = currentTimeFormatted;
      durationElem.textContent = durationFormatted;
    });

    function formatTime(seconds) {
      const minutes = Math.floor(seconds / 60);
      const remainingSeconds = Math.floor(seconds % 60);
      const remainingSecondsFormatted = remainingSeconds < 10 ? `0${remainingSeconds}` : remainingSeconds;

      return `${minutes}:${remainingSecondsFormatted}`;
    }

    // barra de progresso
    
    var progress = document.querySelector('.progress');
    var progressBar = document.querySelector('.progress-bar');

    player.on('timeupdate', function() {
      var currentTime = player.currentTime();
      var duration = player.duration();
      var percent = (currentTime / duration) * 100;

      progress.style.width = percent + '%';
    });

    progressBar.addEventListener('click', function(e) {
      var pos = (e.pageX - (this.offsetLeft + this.offsetParent.offsetLeft)) / this.offsetWidth;
      player.currentTime(player.duration() * pos);
    });

    // Avançar o vídeo de acordo com clique na barra de progresso

    // Adiciona evento de clique na barra de progresso
    progressBar.addEventListener('click', (event) => {
      // Calcula a posição clicada na barra de progresso
      const position = event.offsetX / progressBar.offsetWidth;
      // Atualiza o tempo do vídeo para a posição correspondente
      const newTime = position * player.duration();
      player.currentTime(newTime);
    });

    // Retrocer ou Avançar com as setas do teclado

    // Adiciona função de avançar e retroceder o vídeo com as setas do teclado
    document.addEventListener('keydown', (event) => {
      if (event.code === 'ArrowLeft') {
        player.currentTime(player.currentTime() - 10);
        lastTime = player.currentTime();
      } else if (event.code === 'ArrowRight') {
        player.currentTime(player.currentTime() + 10);
        lastTime = player.currentTime();
      }
    });

    // Adiciona função de atualizar a barra de progresso do vídeo
    setInterval(() => {
      let currentPercent = Math.round((player.currentTime() / player.duration()) * 100);
      let progress = document.querySelector('.video-progress');
      let progressBar = document.querySelector('.progress');
      progress.value = currentPercent;
      progressBar.style.width = `${currentPercent}%`;
    }, 500);

    // Voltar da onde parou

    // armazenar a posição do vídeo quando a página for fechada
    window.addEventListener("beforeunload", function() {
      localStorage.setItem("videoPlayerTime", player.currentTime());
    });

    // restaurar a posição do vídeo quando a página for carregada
    window.addEventListener("load", function() {
      var lastTime = localStorage.getItem("videoPlayerTime");
      if (lastTime) {
        player.currentTime(lastTime);
      }
    });

    // Voltar para o inicio do video se o video for finalizado

    player.ready(function() {
      var lastTime = 0;
      if(localStorage.getItem('lastTime')) {
        lastTime = parseInt(localStorage.getItem('lastTime'));
        player.currentTime(lastTime);
      }
      player.on('timeupdate', function() {
        var currentTime = player.currentTime();
        localStorage.setItem('lastTime', currentTime);
      });
      player.on('ended', function() {
        localStorage.removeItem('lastTime');
      });
    });

    // Ocultar/Mostrar barra superior e controles com movimento do mouse

    // seleciona os elementos que serão ocultados
    const topBar = document.querySelector('.top');
    const controls = document.querySelector('.controls');

    // define o tempo em milissegundos após o qual os elementos serão ocultados
    const timeout = 2000;

    let timeoutId = null;

    // função que oculta os elementos
    function hideControls() {
      topBar.style.opacity = 0;
      controls.style.opacity = 0;
      document.body.style.cursor = 'none';
    }

    // função que exibe os elementos
    function showControls() {
      topBar.style.opacity = 1;
      controls.style.opacity = 1;
      document.body.style.cursor = 'auto';
    }

    // evento que é disparado quando o mouse é movido
    document.addEventListener('mousemove', () => {
      // cancela o timeout anterior
      clearTimeout(timeoutId);
      
      // exibe os elementos
      showControls();
      
      // define um novo timeout para ocultar os elementos
      timeoutId = setTimeout(() => {
        hideControls();
      }, timeout);
    });

    // evento que é disparado quando os elementos são exibidos
    document.addEventListener('mouseenter', () => {
      // cancela o timeout anterior
      clearTimeout(timeoutId);
      
      // exibe os elementos
      showControls();
      
      // define um novo timeout para ocultar os elementos
      timeoutId = setTimeout(() => {
        hideControls();
      }, timeout);
    });

    // evento que é disparado quando os elementos são ocultados
    document.addEventListener('mouseleave', () => {
      // cancela o timeout anterior
      clearTimeout(timeoutId);
      
      // oculta os elementos
      hideControls();
    });

    // rotacionar avançar/retroceder

    const rewindIcon = document.querySelector('.icon.rewind');
    const forwardIcon = document.querySelector('.icon.fast-forward');

    rewindIcon.addEventListener('click', () => {
      rewindIcon.classList.add('rotate');

      // remover a classe 'rotate' após a animação ter terminado
      setTimeout(() => {
        rewindIcon.classList.remove('rotate');
      }, 200);
    });

    forwardIcon.addEventListener('click', () => {
      forwardIcon.classList.add('rotate');

      // remover a classe 'rotate' após a animação ter terminado
      setTimeout(() => {
        forwardIcon.classList.remove('rotate');
      }, 200);
    });

    // icon Volume 

    const volumeIcon = document.querySelector('.volume-icon');
    const volumeRange = document.querySelector('.volume_range');

    volumeRange.addEventListener('input', () => {
      const volume = volumeRange.value;
      
      if (volume == 0) {
        volumeIcon.innerHTML = "volume_off";
      } else if (volume <= 66) {
        volumeIcon.innerHTML = "volume_down";
      } else {
        volumeIcon.innerHTML = "volume_up"
      }
    });
