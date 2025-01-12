chrome.history.onVisited.addListener((historyItem) => {
    console.log('Visited URL:', historyItem.url);
    
    // Check if the URL is a Google search
    if (historyItem.url.startsWith('https://www.google.com/search')) {
      const urlParams = new URLSearchParams((new URL(historyItem.url)).search);
      const query = urlParams.get('q');
      if (query) {
        console.log('Search Query:', query);
      }
    }
  });
  