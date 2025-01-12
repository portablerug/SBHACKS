document.getElementById('start-scan').addEventListener('click', () => {
    window.electron.send('start-scan', {});
  });
  
  window.electron.receive('scan-result', (data) => {
    console.log('Scan Result:', data);
  });
  