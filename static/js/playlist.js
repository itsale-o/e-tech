
const videosPlaylist = document.querySelectorAll(".playlist-video");
const mainVideoDiv = document.querySelector(".main-video-content");
const mainVideo = document.querySelector(".main-video");
const mainInfo = document.querySelector(".main-info");

videosPlaylist.forEach(video => {

    mainVideo.src = videosPlaylist[0].children[0].src;
    mainInfo.innerHTML = videosPlaylist[0].children[1].innerHTML;
    
    videosPlaylist[0].classList.add("active");

    video.addEventListener("click", e =>{
        videosPlaylist.forEach(video => {
            video.classList.remove("active");
        });

        mainVideo.src = video.children[0].src;
        mainInfo.innerHTML = video.children[1].innerHTML;
        video.classList.add("active");
    });
});

