// https://www.youtube.com/watch?v=Jxj_jfh4IDk
chrome.action.onClicked.addListener(function(tab) {
  chrome.tabs.create({
    url: chrome.runtime.getURL('popup.html'),
    active: true
  });
});

const GOOGLE_ORIGIN = 'https://mail.google.com';

chrome.tabs.onUpdated.addListener(async (tabId, info, tab) => {
  if (!tab.url) return;
  const url = new URL(tab.url);
  // Enables the side panel on google.com
  if (url.origin === GOOGLE_ORIGIN) {
    await chrome.sidePanel.setOptions({
      tabId,
      path: 'popup.html',
      enabled: true
    });
  } else {
    // Disables the side panel on all other sites
    await chrome.sidePanel.setOptions({
      tabId,
      enabled: false
    });
  }
});

