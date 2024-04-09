function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tab-content");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tab-link");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    var tabToShow = document.getElementById(tabName);
    if(tabToShow) {
        tabToShow.style.display = "block";
        evt.currentTarget.className += " active";
    } else {
        console.error("Tab content ID not found:", tabName);
    }
}

document.addEventListener("DOMContentLoaded", function() {
    var defaultTab = document.getElementById("defaultOpen");
    if(defaultTab) {
        defaultTab.click();
    } else {
        console.error("Default tab ID not found: defaultOpen");
    }
});