const video_player = document.querySelector('#video_player'),
mainVideo = video_player.querySelector('#main_video'),
progressAreaTime = video_player.querySelector('.progressAreaTime'),
controls = video_player.querySelector('.controls'),
progressArea = video_player.querySelector('.progress-area'),
progress_Bar = video_player.querySelector('.progress-bar'),
fast_rewind = video_player.querySelector('.fast-rewind'),
mouse = video_player.querySelector('.mouse'),
top_banner = video_player.querySelector('.top'),
play_pause = video_player.querySelector('.play_pause'),
pp = video_player.querySelector('.pp'),
fast_foward = video_player.querySelector('.fast-forward'),
volume = video_player.querySelector('.volume'),
volume_range = video_player.querySelector('.volume_range'),
current = video_player.querySelector('.current'),
totalDuration = video_player.querySelector('.duration')
auto_play = video_player.querySelector('.auto-play'),
settingBtn = video_player.querySelector('.settingsBtn'),
picture_in_picture = video_player.querySelector('.picture_in_picture'),
fullscreen = video_player.querySelector('.fullscreen'),
settings = video_player.querySelector('.settings'),
playback = video_player.querySelectorAll('.playback li');


//Função Play
function playVideo() {
    play_pause.innerHTML = "pause";
    play_pause.title = "pause";
    video_player.classList.add("paused");
    mainVideo.play();
  }
  
  // Pause video function
function pauseVideo() {
    play_pause.innerHTML = "play_arrow";
    play_pause.title = "play";
    video_player.classList.remove("paused");
    mainVideo.pause();
  }
  
play_pause.addEventListener("click", () => {
    const isVideoPaused = video_player.classList.contains("paused");
    isVideoPaused ? pauseVideo() : playVideo();
  });
  
mainVideo.addEventListener("play", () => {
    playVideo();
  });
  
mainVideo.addEventListener("pause", () => {
    pauseVideo();
  });
  

//Função Play
function playVideo1() {
    pp.innerHTML = "pause";
    video_player.classList.add("paused");
    mainVideo.play();
  }
  
  // Pause video function
function pauseVideo1() {
    pp.innerHTML = "play_arrow";
    video_player.classList.remove("paused");
    mainVideo.pause();
  }
  
pp.addEventListener("click", () => {
    const isVideoPaused = video_player.classList.contains("paused");
    isVideoPaused ? pauseVideo1() : playVideo1();
  });
  
mainVideo.addEventListener("play", () => {
    playVideo1();
  });
  
mainVideo.addEventListener("pause", () => {
    pauseVideo1();
  });
  

//Função Retroceder

fast_rewind.addEventListener('click', ()=>{
    mainVideo.currentTime -=10;
})

//Função Avançar

fast_foward.addEventListener('click', ()=>{
    mainVideo.currentTime +=10;
})

//Duração completa do vídeo

mainVideo.addEventListener("loadeddata", (e)=>{
    let videoDuration = e.target.duration;
    let totalMin = Math.floor(videoDuration / 60);
    let totalSec = Math.floor(videoDuration % 60);

    totalSec < 10 ? totalSec = "0"+totalSec : totalSec;
    totalDuration.innerHTML = `${totalMin} : ${totalSec}`;
})

//Momento do vídeo

mainVideo.addEventListener('timeupdate', (e)=>{
    let currentVideoTime = e.target.currentTime
    let currentMin = Math.floor(currentVideoTime / 60);
    let currentSec = Math.floor(currentVideoTime % 60);

    currentSec < 10 ? currentSec = "0"+currentSec : currentSec;
    current.innerHTML = `${currentMin} : ${currentSec}`

    videoDuration = e.target.duration
    //Barra de progresso
    let progressWidth = (currentVideoTime / videoDuration) * 100;
    progress_Bar.style.width = `${progressWidth}%`;
})

// Atualizar a hora atual de acordo com a barra de progresso

progressArea.addEventListener('click', (e)=>{
    let videoDuration = mainVideo.duration;
    let progressWidthval = progressArea.clientWidth;
    let ClickOffsetX = e.offsetX;
    mainVideo.currentTime = (ClickOffsetX / progressWidthval) * videoDuration;
})

//Alterar Volume
function changeVolume() {
    mainVideo.volume = volume_range.value / 100;
    if (volume_range.value == 0) {
        volume.innerHTML = "volume_off";
    }else if(volume_range.value < 40){
        volume.innerHTML = "volume_down";
    }else if(40 < volume_range.value < 70 ){
        volume.innerHTML = "volume_down";
    }else {
        volume.innerHTML = "volume_up"
    }
}

function muteVolume() {
    if (volume_range.value == 0) {
        volume_range.value = 80;
        mainVideo.volume = 0.8;
        volume.innerHTML = "volume_up"
    }else{
        volume_range.value = 0;
        mainVideo.volume = 0;
        volume.innerHTML = "volume_off"
    }
}

volume_range.addEventListener('change',()=>{
    changeVolume();
})

volume.addEventListener('click', ()=>{
    muteVolume();
})

// Display Time

progressArea.addEventListener('mousemove', (e)=>{
    let progressWidthval = progressArea.clientWidth;
    let x = e.offsetX;
    progressAreaTime.style.setProperty('--x', `${x}px`);
    progressAreaTime.style.display = "block";
    let videoDuration = mainVideo.duration;
    let progressTime = Math.floor((x/progressWidthval)*videoDuration);
    let currentMin = Math.floor(progressTime / 60);
    let currentSec = Math.floor(progressTime % 60);
    currentSec < 10 ? currentSec = "0"+currentSec : currentSec;
    progressAreaTime.innerHTML = `${currentMin} : ${currentSec}`
})

progressArea.addEventListener('mouseleave', ()=>{
    progressAreaTime.style.display = "none";
})

//Auto Play

auto_play.addEventListener('click',()=>{
    auto_play.classList.toggle('active')
    if(auto_play.classList.contains('active')){
        auto_play.title = "Autoplay está ativo";
    }else{
        auto_play.title = "Autoplay está desligado";
    }
});

mainVideo.addEventListener("ended",()=>{
    if (auto_play.classList.contains('active')) {
        playVideo();
    }else{
        play_pause.innerHTML = "replay";
        play_pause.title = "Replay";
    }
});

// Picture in Picture

picture_in_picture.addEventListener('click',()=>{
    mainVideo.requestPictureInPicture();
});

//Tela Cheia no Botão

fullscreen.addEventListener('click',()=>{
    if (!video_player.classList.contains('openFullScreen')) {
        video_player.classList.add('openFullScreen');
        fullscreen.innerHTML = "fullscreen_exit"
        video_player.requestFullscreen();
        mainVideo.style.margin = "0 0 320px 0";
    }else {
        video_player.classList.remove('openFullScreen');
        fullscreen.innerHTML = "fullscreen"
        document.exitFullscreen();
    }
});

//Tela Cheia com Doble Click

mainVideo.addEventListener('dblclick',()=>{
    if (!video_player.classList.contains('openFullScreen')) {
        video_player.classList.add('openFullScreen');
        fullscreen.innerHTML = "fullscreen_exit"
        video_player.requestFullscreen();
        mainVideo.style.margin = "0 0 320px 0";
    }else {
        video_player.classList.remove('openFullScreen');
        mainVideo.innerHTML = "fullscreen"
        document.exitFullscreen();
    }
});

//Aparecer e sumir controles

mainVideo.addEventListener('click',()=>{
    controls.style.display = "inline";
})

controls.addEventListener('mouseleave',()=>{
    controls.style.display = "none";
})

//Aparecer e sumir banner top

mainVideo.addEventListener('click',()=>{
    top_banner.style.display = "inline";
})

controls.addEventListener('mouseleave',()=>{
    top_banner.style.display = "none";
})

//Aparecer e sumir Mouse

controls.addEventListener('mouseleave',()=>{
    mainVideo.style.cursor = "none"
})

video_player.addEventListener('click',()=>{
    mainVideo.style.cursor = "pointer"
})


//Configurações

settingBtn.addEventListener('click', ()=>{
    settings.classList.toggle('active');
    settingBtn.classList.toggle('active');
})

//Taxa de reprodução

playback.forEach((event)=>{
    event.addEventListener('click',()=>{
        removeActiveClasses();
        event.classList.add('active');
        let speed = event.getAttribute('data-speed');
        mainVideo.playbackRate = speed;
    })
})

function removeActiveClasses(){
    playback.forEach(event => {
        event.classList.remove('active')
    });
}

//Salvar duração do vídeo

window.addEventListener('unload', ()=>{
    let setDuration = localStorage.setItem('duration',`${mainVideo.currentTime}`);
    let setSrc = localStorage.setItem('src',`${mainVideo.getAttribute('src')}`);
})

window.addEventListener('load', ()=>{
    let getDuration = localStorage.getItem('duration');
    let getSrc = localStorage.getItem('src');
    if (getSrc) {
        mainVideo.src = getSrc;
        mainVideo.currentTime = getDuration;
    }
})

mainVideo.addEventListener('contextmenu', (e)=>{
    e.preventDefault();
})

//Mouse move

video_player.addEventListener('mouseover', ()=>{
    controls.classList.add('active')
})

video_player.addEventListener('mouseleave', ()=>{
    if (video_player.classList.contains('paused')){
        if(settingBtn.classList.contains('active')){
            controls.classList.add('active');
        }else{
            controls.classList.remove('active');
        }
    }else {
        controls.classList.add('active')
    }
})

if (video_player.classList.contains('paused')){
    if(settingBtn.classList.contains('active')){
        controls.classList.add('active');
    }else{
        controls.classList.remove('active');
    }
}else {
    controls.classList.add('active')
}

//touch controls mobile

video_player.addEventListener('touchstart', ()=>{
    controls.classList.add('active'),
    setTimeout(() => {
        controls.classList.remove('active')
    }, 8000)
})

video_player.addEventListener('touchmove', ()=>{
    if (video_player.classList.contains('paused')){
        controls.classList.remove('active')
    }else {
        controls.classList.add('active')
    }
})

