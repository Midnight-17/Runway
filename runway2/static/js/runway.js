function makecalendargrid(year,month){
    const MonthStart = new Date(year,month,1).getDay();
    const MonthEnd = new Date(year,month+1,0).getDate();
    const grid = [];


    for (let i = MonthStart-1; i >= 0; i--){
        grid.push({
            date: new Date(year,month-1,MonthEnd-i),
            inMonth: false
        })
    }

    for (let i = 1; i <= MonthEnd; i++){
        grid.push({
            date: new Date(year,month,i),
            inMonth: true
        })
    }
    let nxt = 1 
    while (grid.length < 42){
        grid.push({
            date: new Date(year,month+1,nxt),
            inMonth: false
        })
        nxt++
    }

    return grid;                        
}




//fucntion to format date
function formatDate(d) {
    return d.toLocaleDateString(undefined, {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  }




//defining the function to calculate the days between two dates
function daysBetween(a,b){
    const msPerDay = 24 * 60 * 60 * 1000;
    const start = new Date(a.getFullYear(), a.getMonth(), a.getDate());
    const end = new Date(b.getFullYear(), b.getMonth(), b.getDate());
    return Math.round((end - start) / msPerDay);
}



// geting the current date and making the grid
const now = new Date();
const year = now.getFullYear();
const month = now.getMonth();
const grid = makecalendargrid(year,month);

//make the month appear on top
const monthNames = ['January', 'February', 'March', 'April', 'May', 'June',
                    'July', 'August', 'September', 'October', 'November', 'December'];

const mnth = document.getElementById("monthLabel");
if (mnth) {
  mnth.textContent = monthNames[month]; // month from new Date().getMonth()
}



//exampel exam date
const EXAM_DATE = new Date(2025, 8, 21);


//so here we are wrting the js to render the exam date and the number of day to exam 
const daysToExam = Math.max(0, daysBetween(now, EXAM_DATE));
document.getElementById('daysToExam').textContent = String(daysToExam);
document.getElementById('examDateHint').textContent = `Exam: ${formatDate(EXAM_DATE)}`;




//adding the headers to the calendar grid
const calendar = document.getElementById('calendar');
const weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
weekdays.forEach(w => {
  const el = document.createElement('div');
  el.className = 'weekday';
  el.textContent = w;
  calendar.appendChild(el);
});






grid.forEach(({date,inMonth}) => {


  






    //looping through the 42 cells in the grid
    const cell = document.createElement('div');
    cell.className = 'day' + (inMonth ? '' : ' muted');
    
  
    /// Define first 10 days as completed
    const completions = [];
    for (let i = 1; i <= 10; i++) completions.push(i);





    //adding the number to each cell
    const num = document.createElement('div');
    num.className = 'num';
    num.textContent = String(date.getDate());
    cell.appendChild(num);  

    //adding the chip to each cell
    const chip = document.createElement('div');
    chip.className = 'chip';
    cell.appendChild(chip);

    //adding a today highlight
    const isToday = date.toDateString() === now.toDateString();
    if (isToday) {cell.classList.add('today');}
    
    //adding a completed highlight
    if (inMonth && completions.includes(date.getDate())) {
        cell.classList.add('completed');
    }


    // adding the cell to the calendar (num already appended before chip above)
    calendar.appendChild(cell);

    
});

//getting all the thing
const trackBtn = document.getElementById("trackBtn");
const videoInput = document.getElementById("videoInput");
const uploadForm = document.getElementById("uploadForm");
const videoGallery = document.getElementById("videoGallery");

trackBtn.addEventListener("click", () => {
  videoInput.click(); // open file picker
});

videoInput.addEventListener("change", () => {
  const formData = new FormData(uploadForm);
  fetch(uploadForm.action, {
    method: "POST",
    body: formData,
    headers: {
      "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
    },
  })
    .then((res) => res.json())
    .then((data) => {
        if (data.video_url) {
            // Find today's cell
            const todayCell = document.querySelector(".day.today");
            if (todayCell) {
                // Remove any existing video link first
                const existingLink = todayCell.querySelector(".video-link");
                if (existingLink) existingLink.remove();

                // Create the link element
                const videoLink = document.createElement("a");
                videoLink.textContent = "Access video";
                videoLink.href = data.video_url;
                videoLink.target = "_blank";
                videoLink.className = "video-link"; // for styling
                videoLink.style.color = "#66cccc";       // ✅ this is correct
                videoLink.style.width = "80%";           // ✅ needs to be set via style object
                videoLink.style.display = "block";       // optional, makes width work properly


                // Append the link inside today's cell
                todayCell.appendChild(videoLink);
            }
        } else {
            alert("Upload failed.");
        }
    })
    .catch((err) => console.error(err));
});
