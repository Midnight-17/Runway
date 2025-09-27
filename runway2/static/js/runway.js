let completions = [];  // will store the array from Django // Store video URLs by date (day of month)
const now = new Date();
const year = now.getFullYear();
const currentMonth = now.getMonth();
const calendar = document.getElementById('calendar');
const weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
const monthNames = ['January', 'February', 'March', 'April', 'May', 'June',
                    'July', 'August', 'September', 'October', 'November', 'December'];




function renderCalendar() {
  if (!calendar) return;
  // Clear any existing content
  calendar.innerHTML = '';

  // Update month label
  const mnth = document.getElementById("monthLabel");
  if (mnth) {
    mnth.textContent = monthNames[currentMonth];
  }

  // Weekday headers
  weekdays.forEach(w => {
    const el = document.createElement('div');
    el.className = 'weekday';
    el.textContent = w;
    calendar.appendChild(el);
  });

  // Build the 6x7 calendar grid for the current month
  const grid = makecalendargrid(year, currentMonth);
  grid.forEach(({ date, inMonth }) => {
    const dayNumber = date.getDate();
    const hasVideo = Video_Progress_[dayNumber]; // Check if this day has a video
    
    // Create cell container (either div or anchor)
    let cell;
    if (hasVideo) {
      // If there's a video, make it a clickable link
      cell = document.createElement('a');
      cell.href = hasVideo;
      cell.target = '_blank'; // Open in new tab
      cell.style.textDecoration = 'none';
      cell.style.color = 'inherit';
    } else {
      // Regular div if no video
      cell = document.createElement('div');
    }
    
    cell.className = 'day' + (inMonth ? '' : ' muted');

    // Day number
    const num = document.createElement('div');
    num.className = 'num';
    num.textContent = String(dayNumber);
    cell.appendChild(num);

    // Chip
    const chip = document.createElement('div');
    chip.className = 'chip';
    cell.appendChild(chip);

    // Today highlight
    const isToday = date.toDateString() === now.toDateString();
    if (isToday) { cell.classList.add('today'); }

    // Completed highlight (only mark if the date is in the current month)
    if (inMonth && completions.includes(dayNumber)) {
      cell.classList.add('completed');
    }



    calendar.appendChild(cell);
  });
}

fetch(`/monthly-progress/${studentName}`)
  .then(res => res.json())
  .then(data => {
    completions = data.completions || [];
    Video_Progress_ = data.Video_Progress
    console.log("Loaded progress:", completions);
    console.log(Video_Progress_);
    // After fetching, render the calendar
    renderCalendar();
  })
  .catch(err => console.error("Error fetching progress:", err));

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

//function to format date
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

//example exam date
const EXAM_DATE = new Date(2025, 8, 21);

//so here we are writing the js to render the exam date and the number of day to exam 
const daysToExam = Math.max(0, daysBetween(now, EXAM_DATE));
document.getElementById('daysToExam').textContent = String(daysToExam);
document.getElementById('examDateHint').textContent = `Exam: ${formatDate(EXAM_DATE)}`;

//getting all the things
const trackBtn = document.getElementById("trackBtn");
const videoInput = document.getElementById("videoInput");
const uploadForm = document.getElementById("uploadForm");
const videoGallery = document.getElementById("videoGallery");

if (trackBtn && videoInput) {
  trackBtn.addEventListener("click", () => {
    videoInput.click();
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
              // Update completions
              if (data.Month_Progress) {
                  completions = data.Month_Progress;
              }
              
              // Store the video URL for today's date
              const today = now.getDate();
              Video_Progress_[today] = data.video_url;;
              
              // Re-render the entire calendar to show the new clickable cell
              renderCalendar();
              
              console.log("Video uploaded successfully for day:", today);
          } else {
              alert("Upload failed.");
          }
      })
      .catch((err) => console.error(err));
  });


}




//get the button
const studentButtons = document.querySelectorAll('.student-btn');

// mainStudent should be your current selected student
let mainStudent = studentName; // studentName declared outside

studentButtons.forEach(button => {
  const studentName_ = button.dataset.student;

  // Initial highlight
  if (mainStudent === studentName_) {
    button.style.color = "#00e0d5";
    button.style.borderColor = "#00e0d5";
  }

  button.addEventListener("click", () => {
    // Update mainStudent
    mainStudent = studentName_;

    // Update button highlights
    studentButtons.forEach(btn => {
      if (btn.dataset.student === mainStudent) {
        btn.style.color = "#00e0d5";
        btn.style.borderColor = "#00e0d5";
      } else {
        btn.style.color = "";        // reset color
        btn.style.borderColor = "";  // reset border
      }
    });

    // Update calendar
    changeCalendar(mainStudent);
  });
});


function changeCalendar(studentName) {
  fetch(`/monthly-progress/${studentName}`)
  .then(res=>res.json())
  .then((data)=>{
    completions = data.completions || [];
    Video_Progress_ = data.Video_Progress
    console.log("Loaded progress:", completions);
    console.log(Video_Progress_);
    // After fetching, render the calendar
    renderCalendar();
  })
  // your calendar logic here
}



const changeDateBtn = document.getElementById("changeDateBtn");
const examDateInput = document.getElementById("examDateInput");
const examRow = document.querySelector(".exam-row");

changeDateBtn.addEventListener("click", () => {
  examDateInput.style.display = "inline-block";
  changeDateBtn.style.display = "none";

// hide label, show input
  examDateInput.focus();
});

examDateInput.addEventListener("change", (e) => {
  const newDate = new Date(e.target.value);
  if (!isNaN(newDate)) {
    document.getElementById("examDateHint").textContent = `Exam: ${formatDate(newDate)}`;
    EXAM_DATE.setTime(newDate.getTime());
    const daysToExam = Math.max(0, daysBetween(new Date(), EXAM_DATE));
    document.getElementById('daysToExam').textContent = String(daysToExam);
  }
  examDateInput.style.display = "none";
  changeDateBtn.style.display = "inline-block";
   // hide input, show label again
});


