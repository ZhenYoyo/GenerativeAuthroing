
$(document).ready(function(){
  setInterval(function(){

     $.ajax({
      url: '/worldcard',
      type: 'GET',
      dataType: 'json',
      success: function(data){
          $('#worldcard').text(data.value);
          //$('#worldcontent').text(data.worldlist);
          createDraggableCards(data.value, 'worldcard', '#FF69B4', data.worldlist); 
      }
     });
  

      $.ajax({
          url: '/charactercard',
          type: 'GET',
          dataType: 'json',
          success: function(data){
              $('#charactercard').text(data.value);
              // $('#charactercontent').text(data.characterlist);
              createDraggableCards(data.value, 'charactercard', '#3CB371', data.characterlist); 
          }
      });

      $.ajax({
          url: '/narratorcard',
          type: 'GET',
          dataType: 'json',
          success: function(data){
              $('#narratorcard').text(data.value);
              // $('#narratorcontent').text(data.narratorlist);
              createDraggableCards(data.value, 'narratorcard', '#FFB6C1', data.narratorlist); 
          }
      });

      $.ajax({
          url: '/inputcard',
          type: 'GET',
          dataType: 'json',
          success: function(data){
              // $('#inputcontent').text(data.inputlist);
              createDraggableCards(data.value, 'inputcard', '#FFA500', data.inputlist); 
          }
      });

    $.ajax({
      url: '/updatenarrative',
      type: 'GET',
      dataType: 'json',
      success: function(data){
          $('#lalala').text(data.value);
      }
  });
  

  }, 1000);  
});


// $(document).ready(function(){
//   setInterval(function(){

//      $.ajax({
//       url: '/worldcard',
//       type: 'GET',
//       dataType: 'json',
//       success: function(data){
//           $('#worldcard').text(data.value);
//           // $('#worldcontent').text(data.worldlist);
//           createDraggableCards(data.value, 'worldcard', '#FF69B4', data.worldlist); 
//       }
//      });
  

//       $.ajax({
//           url: '/charactercard',
//           type: 'GET',
//           dataType: 'json',
//           success: function(data){
//               $('#charactercard').text(data.value);
//               // $('#charactercontent').text(data.characterlist);
//               createDraggableCards(data.value, 'charactercard', '#3CB371', data.characterlist); 
//           }
//       });

//       $.ajax({
//           url: '/narratorcard',
//           type: 'GET',
//           dataType: 'json',
//           success: function(data){
//               $('#narratorcard').text(data.value);
//               // $('#narratorcontent').text(data.narratorlist);
//               createDraggableCards(data.value, 'narratorcard', '#FFB6C1', data.narratorlist); 
//           }
//       });

//       $.ajax({
//           url: '/inputcard',
//           type: 'GET',
//           dataType: 'json',
//           success: function(data){
//               // $('#inputcontent').text(data.inputlist);
//               createDraggableCards(data.value, 'inputcard', '#FFA500', data.inputlist); 
//           }
//       });



//       $.ajax({
//         url: '/process',
//         type: 'GET',
//         dataType: 'json',
//         success: function(datasend){
//             updateNarrative(datasend.aioutput); 
//         }
//     });
//   }, 1000);  
// });



// page1

var worldsettingList =[
  "Enchanted Forest: A mystical forest shrouded in enchantment, with towering ancient trees, sparkling streams, and glowing flora. Sunlight filters through the dense canopy, casting ethereal hues across the landscape. Magical creatures roam freely, and whispers of forgotten spells fill the air.",
  "A bustling metropolis of gleaming skyscrapers, advanced technology, and neon lights. Flying cars zip through the skies, holographic advertisements dance on every corner, and automated drones navigate the cityscape. The atmosphere hums with energy and innovation.",
   "Decaying ruins of a long-lost civilization, nestled deep within an overgrown jungle. Crumbling stone structures, intricate carvings, and moss-covered artifacts tell tales of a forgotten era. The air is heavy with mystery and echoes of the past."
  ]
  
var characterList =[
"Luna: Luna is a wise and mysterious sorceress with long flowing robes and a staff adorned with glowing crystals. She possesses ancient knowledge and a calm demeanor. Her eyes sparkle with hidden powers, and her words resonate with wisdom and guidance.",
"Max: Max is a curious and adventurous young explorer. He wears a weathered hat, a tattered explorer's jacket, and carries a map and compass. With a mischievous grin, he embodies the spirit of a fearless adventurer, always seeking new discoveries and thrills.",
"Aurora: Aurora is a kind-hearted and compassionate fairy with shimmering wings and a radiant aura. She spreads joy and healing with her gentle touch and soothing voice. Her presence brings a sense of tranquility and hope to those around her."
]
  
var narratorList = [
  "Descriptive: The narrator provides vivid descriptions of the surroundings, characters, and events, painting a detailed picture for the audience. They engage the audience's senses by describing sights, sounds, smells, and textures.",
  "Engaging: The narrator uses a dynamic and expressive tone, capturing the audience's attention and creating a sense of excitement. They employ rhetorical questions, exclamations, and varying pacing to keep the audience engaged and interested.",
  "Reflective: The narrator offers introspective and contemplative insights, delving into the characters' thoughts and emotions. They provide commentary on the themes and deeper meanings of the story, encouraging the audience to reflect on the narrative's messages."
  ]
  
var variableList =[
    "darkmatter",
    "lightinstensity",
    "water"
  ]

var variableDesList =[
    "denoted by 1-10, more darkmatter, the story becomes more mysterious",
    "denoted by 1-10, more light intensity, the story becomes more bright and hopeful",
    "a boolean variable, if water is present, the story will mentioned water"
  ]

var currentIndex = 0;  

function populateInputFields() {
 
  if (currentIndex < 4) {
    var currentworld = worldsettingList[currentIndex];
    var currentcharacter = characterList[currentIndex];
    var currentnarrator = narratorList[currentIndex];
    var currentvariable = variableList[currentIndex];
    var currentvariabledes = variableDesList[currentIndex];

    document.getElementById("typing-bar_world-1").value = currentworld;
    document.getElementById("typing-bar_world-2").value = currentcharacter;
    document.getElementById("typing-bar_world-5").value = currentnarrator;
    document.getElementById("typing-bar_world-3").value = currentvariable;
    document.getElementById("typing-bar_world-4").value = currentvariabledes;
    currentIndex++;  
  }
}

function updateworld(barNumber) {
  // added

  const typingBar = document.getElementById(`typing-bar_world-${barNumber}`);
  const output = document.getElementById(`output-world-${barNumber}`);

  const entry = document.createElement("div");
  entry.className = "entry";

  const deleteButton = document.createElement("button");
  deleteButton.className = "delete-button";
  deleteButton.innerHTML = "−";
  entry.appendChild(deleteButton);

  const entryText = document.createElement("span");
  entryText.innerHTML = typingBar.value;
  entry.appendChild(entryText);

  deleteButton.onclick = function () {
    entry.remove();

 fetch('/removeworld', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ value:entryText.innerHTML, id:barNumber  })
  })
    .then(response => response.json())
    .then(data => {
    });
  };
  

  output.appendChild(entry);

  // Send input data to the Python server
  fetch('/world', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ text: typingBar.value , id:barNumber})
  })
    .then(response => response.json())
    .then(data => {
      
    });

  typingBar.value = "";
}


function updatevariable(barNumberVariable) {
  // function updateworld(barNumber) {
    // added
    const barNumber4 = barNumberVariable + 1;
  
  
    const typingBar = document.getElementById(`typing-bar_world-${barNumberVariable}`);
    const output = document.getElementById(`output-world-${barNumberVariable}`);
  
    const entry = document.createElement("div");
    entry.className = "entry";
  
    const deleteButton = document.createElement("button");
    deleteButton.className = "delete-button";
    deleteButton.innerHTML = "−";
    entry.appendChild(deleteButton);
  
    const entryText = document.createElement("span");
    entryText.innerHTML = typingBar.value;
    entry.appendChild(entryText);
  
    deleteButton.onclick = function () {
      entry.remove();
  
      // added
      const entry4 = document.getElementById(`output-world-${barNumber4}`);
      if (entry4) {
        entry4.remove();
        // 发送删除请求给服务器（如果需要）
        fetch('/removeworld', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ value: entryText.innerHTML, id: barNumber4 })
        })
          .then(response => response.json())
          .then(data => {
            // 处理返回的数据（如果需要）
          });
      }
  
  
   fetch('/removeworld', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ value:entryText.innerHTML, id:barNumberVariable})
    })
      .then(response => response.json())
      .then(data => {
      });
    };
    
    output.appendChild(entry);
  
    // Send input data to the Python server
    fetch('/world', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ text: typingBar.value , id:barNumberVariable})
    })
      .then(response => response.json())
      .then(data => {
        
      });
  
    typingBar.value = "";
  }

function resetVariablesOnRefresh() {
  // Check if the page is being accessed for the first time or after a refresh
  if (performance.navigation.type === 1) {
    // Clear all stored variable values
    fetch('/reset', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({})
  })
    .then(response => response.json())
    .then(data => {
    });

  }
}


//page2

function createDraggableCards(cardCount, cardType, color, textlist) {
  var cardContainer = $('#' + cardType + 'Container');
  var textContainer = $('#textContainer');
  cardContainer.empty(); 

  for (var i = 1; i <= cardCount; i++) {
      var card = $('<div class="draggable-card">' + cardType + ' Card ' + i + '</div>');
      card.css('background-color', color); 
      card.draggable(); 
      card.data('index', i-1); 

      card.click(function() {
        var index = $(this).data('index'); 
        var cardText = textlist[index]; 
        textContainer.text("details:"+ cardText); 
      });

      cardContainer.append(card); 
  }
}

// page 3

function updateHistory(barNumber) {
  const typingBar = document.getElementById(`typing-bar-${barNumber}`);
  const outputSection = document.getElementById(`output-section-${barNumber}`);
  const entry = document.createElement("div");
  entry.className = "entry";

  const deleteButton = document.createElement("button");
  deleteButton.className = "delete-button";
  deleteButton.innerHTML = "−";
  entry.appendChild(deleteButton);

  const entryText = document.createElement("span");
  entryText.innerHTML = typingBar.value;
  entry.appendChild(entryText);
  deleteButton.onclick = function () {
    entry.remove();
  };

  outputSection.appendChild(entry);
  // Send input data to the Python server
  fetch('/process', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    //body: JSON.stringify({ text: typingBar.value })
    body: JSON.stringify({text: typingBar.value , id:barNumber})
  })
    .then(response => response.json())
    .then(data => {
// entryText.innerHTML = data.output;
    });
  typingBar.value = "";
}


function sendGenerateData() {
  fetch('/process', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ text:"generate", id:5})
  })
  .then(response => response.json())
  .then(data => {
      console.log(':', data);
  })
  .catch(error => {
      console.error('error', error);
  });
}


// others


function showNextPage() {
  document.getElementById('page-1').classList.remove('active');
  document.getElementById('page-2').classList.add('active');
  document.getElementById('page-3').classList.remove('active');
}

function showPreviousPage() {
  document.getElementById('page-2').classList.remove('active');
  document.getElementById('page-1').classList.add('active');
  document.getElementById('page-3').classList.remove('active');
}


function showNextPage2() {
  document.getElementById('page-1').classList.remove('active');
  document.getElementById('page-2').classList.remove('active');
  document.getElementById('page-3').classList.add('active');
}

function showPreviousPage2() {
  document.getElementById('page-1').classList.remove('active');
  document.getElementById('page-3').classList.remove('active');
  document.getElementById('page-2').classList.add('active');
}


function onPageLoadOrRefresh() {
  
  if (performance.navigation.type === 1 || performance.navigation.type === 0) {
    // Perform actions for first page visit or refresh
     fetch('/reset', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({})
  })
    .then(response => response.json())
    .then(data => {
    });

    // Reset variables, initialize state, etc.
    // Example: localStorage.clear();
  }
}

document.addEventListener("DOMContentLoaded", onPageLoadOrRefresh);

