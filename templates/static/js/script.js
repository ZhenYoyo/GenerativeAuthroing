

function showNextPage() {
  document.getElementById('page-1').classList.remove('active');
  document.getElementById('page-2').classList.add('active');
}

function showPreviousPage() {
  document.getElementById('page-2').classList.remove('active');
  document.getElementById('page-1').classList.add('active');
}


$(document).ready(function(){
  setInterval(function(){

     $.ajax({
      url: '/worldcard',
      type: 'GET',
      dataType: 'json',
      success: function(data){
          $('#worldcard').text(data.value);
          // $('#worldcontent').text(data.worldlist);
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
              $('#inputcard').text(data.value);
              // $('#inputcontent').text(data.inputlist);
              createDraggableCards(data.value, 'inputcard', '#FFA500', data.inputlist); 
          }
      });

  }, 1000);  
});


function createDraggableCards(cardCount, cardType, color, textlist) {
  var cardContainer = $('#' + cardType + 'Container');
  var textContainer = $('#textContainer');
  cardContainer.empty(); // 清空容器中的内容

  for (var i = 1; i <= cardCount; i++) {
      var card = $('<div class="draggable-card">' + cardType + ' Card ' + i + '</div>');
      card.css('background-color', color); // 设置背景颜色
      card.draggable(); // 添加可拖动功能
      card.data('index', i-1); // 将索引存储在卡片的数据中

      card.click(function() {
        var index = $(this).data('index'); // 获取卡片的索引
        var cardText = textlist[index]; // 根据索引获取对应的文本
        textContainer.text("details:"+ cardText); // 在textContainer中显示文本
      });

      cardContainer.append(card); // 将卡片添加到容器中

  }
}



function updateHistory(barNumber) {
  const typingBar = document.getElementById(`typing-bar-${barNumber}`);
  const outputSection = document.getElementById("output-section");
const entry = document.createElement("div");
  entry.className = "entry";

  const deleteButton = document.createElement("button");
  deleteButton.className = "delete-button";
  deleteButton.innerHTML = "−";
  entry.appendChild(deleteButton);

  const entryText = document.createElement("span");
  entry.appendChild(entryText);
  deleteButton.onclick = function () {
    entry.remove();
  };
  // Send input data to the Python server
  fetch('/process', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ text: typingBar.value })
  })
    .then(response => response.json())
    .then(data => {
entryText.innerHTML = data.output;
    });
  outputSection.appendChild(entry);
  typingBar.value = "";
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