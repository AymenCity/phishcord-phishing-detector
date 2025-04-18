// https://www.youtube.com/watch?v=Jxj_jfh4IDk
chrome.action.onClicked.addListener(function(tab) {
  chrome.tabs.create({
    url: chrome.runtime.getURL('popup.html'),
    active: true
  });
});

