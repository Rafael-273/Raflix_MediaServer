const player = videojs('my-video');
let lastTime = 0;

player.on('loadedmetadata', function() {
  const playButton = document.querySelector('.play_pause');
  const iconPausePlay = document.querySelector('.pause-play');

  playButton.addEventListener('click', function() {
    if (player.paused()) {
      player.play();
      iconPausePlay.innerHTML = "play_arrow";
    } else {
      player.pause();
      iconPausePlay.innerHTML = "pause";
    }
  });

  player.on('click', function() {
    if (this.paused()) {
      this.play();
      iconPausePlay.innerHTML = "play_arrow";
    } else {
      this.pause();
      iconPausePlay.innerHTML = "pause";
    }
  });

  document.addEventListener('keydown', function(event) {
    if (event.code === 'Space') {
      event.preventDefault();
      if (player.paused()) {
        player.play();
        iconPausePlay.innerHTML = "pause";
      } else {
        player.pause();
        iconPausePlay.innerHTML = "play_arrow";
      }
    }
  });

  document.querySelector('.rewind').addEventListener('click', function() {
    player.currentTime(player.currentTime() - 10);
  });

  document.querySelector('.fast-forward').addEventListener('click', function() {
  
    console.log(player.currentTime()); // Valor atual do currentTime
  
    player.currentTime(20); // Definindo o currentTime como 20 segundos
  
    console.log(player.currentTime()); // Novo valor do currentTime
  
    player.currentTime('20.0'); // Definindo o currentTime como uma string '20.0' (o Video.js converte automaticamente para número)
  
    console.log(player.currentTime()); // Novo valor do currentTime
  });
  

  const volumeControl = document.querySelector(".volume_range");

  volumeControl.addEventListener("input", () => {
    const volumeValue = volumeControl.value / 100;
    player.volume(volumeValue);
  });

  const pipButton = document.querySelector(".picture-in-picture");

  pipButton.addEventListener("click", function() {
    if (document.pictureInPictureElement === player) {
      document.exitPictureInPicture();
    } else {
      player.requestPictureInPicture();
    }
  });

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

  const video = document.querySelector('video');

  video.addEventListener('dblclick', () => {
    if (document.fullscreenElement) {
      document.exitFullscreen();
    } else {
      video.requestFullscreen();
    }
  });

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
    const hours = Math.floor(seconds / 3600);
    const remainingMinutes = Math.floor((seconds % 3600) / 60);
    const remainingSeconds = Math.floor(seconds % 60);
  
    const hoursFormatted = hours < 10 ? `0${hours}` : hours;
    const minutesFormatted = remainingMinutes < 10 ? `0${remainingMinutes}` : remainingMinutes;
    const secondsFormatted = remainingSeconds < 10 ? `0${remainingSeconds}` : remainingSeconds;
  
    return `${hoursFormatted}:${minutesFormatted}:${secondsFormatted}`;
  }  

  const progress = document.querySelector('.progress');
  const progressBar = document.querySelector('.progress-bar');

  player.on('timeupdate', function() {
    const currentTime = player.currentTime();
    const duration = player.duration();
    const percent = (currentTime / duration) * 100;

    progress.style.width = percent + '%';
  });

  progressBar.addEventListener('click', function(e) {
    const pos = (e.pageX - (this.offsetLeft + this.offsetParent.offsetLeft)) / this.offsetWidth;
    player.currentTime(player.duration() * pos);
  });

  progressBar.addEventListener('click', (event) => {
    const position = event.offsetX / progressBar.offsetWidth;
    const newTime = position * player.duration();
    player.currentTime(newTime);
  });

  document.addEventListener('keydown', (event) => {
    if (event.code === 'ArrowLeft') {
      player.currentTime(player.currentTime() - 10);
      lastTime = player.currentTime();
    } else if (event.code === 'ArrowRight') {
      player.currentTime(player.currentTime() + 10);
      lastTime = player.currentTime();
    }
  });

  setInterval(() => {
    const currentPercent = (player.currentTime() / player.duration()) * 100;
    const progressBar = document.querySelector('.progress');
    progressBar.style.width = `${currentPercent}%`;
  }, 500);

  window.addEventListener("beforeunload", function() {
    localStorage.setItem("videoPlayerTime", player.currentTime());
  });

  window.addEventListener("load", function() {
    const lastTime = localStorage.getItem("videoPlayerTime");
    if (lastTime) {
      player.currentTime(lastTime);
    }
  });

  player.ready(function() {
    let lastTime = 0;
    if (localStorage.getItem('lastTime')) {
      lastTime = parseInt(localStorage.getItem('lastTime'));
      player.currentTime(lastTime);
    }
    player.on('timeupdate', function() {
      const currentTime = player.currentTime();
      localStorage.setItem('lastTime', currentTime);
    });
    player.on('ended', function() {
      localStorage.removeItem('lastTime');
    });
  });

  const topBar = document.querySelector('.top');
  const controls = document.querySelector('.controls');
  const timeout = 2000;

  let timeoutId = null;

  function hideControls() {
    topBar.style.opacity = 0;
    controls.style.opacity = 0;
    document.body.style.cursor = 'none';
  }

  function showControls() {
    topBar.style.opacity = 1;
    controls.style.opacity = 1;
    document.body.style.cursor = 'auto';
  }

  document.addEventListener('mousemove', () => {
    clearTimeout(timeoutId);
    showControls();
    timeoutId = setTimeout(() => {
      hideControls();
    }, timeout);
  });

  document.addEventListener('mouseenter', () => {
    clearTimeout(timeoutId);
    showControls();
    timeoutId = setTimeout(() => {
      hideControls();
    }, timeout);
  });

  document.addEventListener('mouseleave', () => {
    clearTimeout(timeoutId);
    hideControls();
  });

  const rewindIcon = document.querySelector('.icon.rewind');
  const forwardIcon = document.querySelector('.icon.fast-forward');

  rewindIcon.addEventListener('click', () => {
    rewindIcon.classList.add('rotate');
    setTimeout(() => {
      rewindIcon.classList.remove('rotate');
    }, 200);
  });

  forwardIcon.addEventListener('click', () => {
    forwardIcon.classList.add('rotate');
    setTimeout(() => {
      forwardIcon.classList.remove('rotate');
    }, 200);
  });

  const volumeIcon = document.querySelector('.volume-icon');
  const volumeRange = document.querySelector('.volume_range');

  volumeRange.addEventListener('input', () => {
    const volume = volumeRange.value;

    if (volume == 0) {
      volumeIcon.innerHTML = "volume_off";
    } else if (volume <= 66) {
      volumeIcon.innerHTML = "volume_down";
    } else {
      volumeIcon.innerHTML = "volume_up";
    }
  });
});