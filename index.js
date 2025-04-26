// parameter videoData is a json string
// returns undefined
const makeVideoGoOnScreen = (videoDataJSON) => {
  const video_data_list = JSON.parse(videoDataJSON);
  const element = document.getElementById('video-feed');

  for (const video_info of video_data_list) {
    element.innerHTML += "<p>" + video_info.timestamp + "</p>";
    element.innerHTML += "<p>" + video_info.filename + "</p>";
    
    // if we modify the html to add a new video element, the browser will automatically
    // download the video when it is running the new html code we're adding here  
    element.innerHTML += `<video controls src="/videos/${video_info.filename}"></video>`;
  }


}


// Just leave this at the bottom...
const p1 = fetch("http://localhost:8000/video-list.json");
const p2 = p1.then((response) => {
  const somePromise = response.text();
  return somePromise;
});
p2.then(makeVideoGoOnScreen);