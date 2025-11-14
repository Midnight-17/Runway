function switchTab(tab) {
    const studentForm = document.getElementById('student-form');
    const teacherForm = document.getElementById('teacher-form');
    const studentTab = document.getElementById('student-tab');
    const teacherTab = document.getElementById('teacher-tab');
    const underline = document.getElementById('underline');

    if (tab === 'student') {
        studentForm.classList.remove('hidden-form');
        studentForm.classList.add('active-form');
        teacherForm.classList.add('hidden-form');
        teacherForm.classList.remove('active-form');

        studentTab.classList.add('active-tab');
        teacherTab.classList.remove('active-tab');

        underline.style.left = '0';
    } else {
        teacherForm.classList.remove('hidden-form');
        teacherForm.classList.add('active-form');
        studentForm.classList.add('hidden-form');
        studentForm.classList.remove('active-form');

        teacherTab.classList.add('active-tab');
        studentTab.classList.remove('active-tab');

        underline.style.left = '50%';
    }
}
