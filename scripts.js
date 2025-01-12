document.getElementById('config-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const selectedOptions = [];
    const checkboxes = document.querySelectorAll('input[name="option"]:checked');
    checkboxes.forEach((checkbox) => {
      selectedOptions.push(checkbox.value);
    });
  
    console.log('Selected Apps:', selectedOptions);
  
    document.body.innerHTML = '<div id="config-app"><h1>Your Automated Tasks</h1><div id="tasks"></div></div>';
  
    const tasksDiv = document.getElementById('tasks');
    if (selectedOptions.length > 0) {
      const ul = document.createElement('ul');
      selectedOptions.forEach(option => {
        const li = document.createElement('li');
        li.textContent = option;
        ul.appendChild(li);
      });
      tasksDiv.appendChild(ul);
    } else {
      tasksDiv.textContent = 'No tasks selected';
    }
  
    selectedOptions.forEach(option => {
      if (option === 'Visual Studio Code') {
        listenToVSCode();
      } else if (option === 'Google Chrome') {
        listenToChrome();
      } else if (option === 'Gmail') {
        listenToGmail();
      } else if (option === 'Unity') {
        listenToUnity();
      } else if (option === 'Netflix') {
        listenToNetflix();
      } else if (option === 'Matlab') {
        listenToMatlab();
      }
    });
  });
  
  function listenToVSCode() {
    console.log('Listening to Visual Studio Code...');
  }
  
  function listenToChrome() {
    console.log('Listening to Google Chrome...');
  }
  
  function listenToGmail() {
    console.log('Listening to Gmail...');
    gapi.client.gmail.users.messages.list({
      'userId': 'me',
      'maxResults': 10
    }).then(response => {
      console.log(response.result);
    });
  }
  
  function listenToUnity() {
    console.log('Listening to Unity...');
  }
  
  function listenToNetflix() {
    console.log('Listening to Netflix...');
  }
  
  function listenToMatlab() {
    console.log('Listening to Matlab...');
  }
  
  function handleClientLoad() {
    gapi.load('client:auth2', initClient);
  }
  
  function initClient() {
    gapi.client.init({
      apiKey: 'YOUR_API_KEY',
      clientId: 'YOUR_CLIENT_ID',
      discoveryDocs: ["https://www.googleapis.com/discovery/v1/apis/gmail/v1/rest"],
      scope: 'https://www.googleapis.com/auth/gmail.readonly'
    }).then(() => {
      gapi.auth2.getAuthInstance().signIn().then(() => {
        console.log('Signed in and Gmail API loaded');
      });
    });
  }
  
  window.onload = handleClientLoad;
  