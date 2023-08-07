var xValues = [];
var yValues = [];
const contestants = document.querySelectorAll('.contestant');
const votes = document.querySelectorAll('.votes');
contestants.forEach(contestant => {
    // Perform actions for each contestant using JavaScript
    xValues.push(contestant.innerText)
});

votes.forEach(vote => {
    // Perform actions for each contestant using JavaScript
    yValues.push(vote.innerText)
});

barColors = ["blue", "red", "green", "purple", "orange", "black"]
new Chart("myChart", {
type: "bar",
data: {
labels: xValues,
datasets: [{
backgroundColor: barColors,
data: yValues
}]
},
options: {
legend: {display: false},
scales: {
yAxes: [{
ticks: {
  beginAtZero: true
}
}],
}
}
});