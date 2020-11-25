// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

function number_format(number, decimals, dec_point, thousands_sep) {
  // *     example: number_format(1234.56, 2, ',', ' ');
  // *     return: '1 234,56'
  number = (number + '').replace(',', '').replace(' ', '');
  var n = !isFinite(+number) ? 0 : +number,
    prec = !isFinite(+decimals) ? 0 : Math.abs(decimals),
    sep = (typeof thousands_sep === 'undefined') ? ',' : thousands_sep,
    dec = (typeof dec_point === 'undefined') ? '.' : dec_point,
    s = '',
    toFixedFix = function(n, prec) {
      var k = Math.pow(10, prec);
      return '' + Math.round(n * k) / k;
    };
  // Fix for IE parseFloat(0.55).toFixed(0) = 0;
  s = (prec ? toFixedFix(n, prec) : '' + Math.round(n)).split('.');
  if (s[0].length > 3) {
    s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep);
  }
  if ((s[1] || '').length < prec) {
    s[1] = s[1] || '';
    s[1] += new Array(prec - s[1].length + 1).join('0');
  }
  return s.join(dec);
}
$(function() {
     $('#upload-file-btn').click(function() {

         var form_data = new FormData($('#upload-file')[0]);
         $.ajax({
             type: 'POST',
             url: '/uploadajax',
             data: form_data,
             contentType: false,
             cache: false,
             processData: false,
             async: false,
             success: function(response) {
                 alert('!')

                 document.getElementById("logCount").innerText = response['logCount'];
                 document.getElementById("hostCount").innerText = response['hostCount'];
                 document.getElementById("faultCount").innerText = response['faultCount'];


                 var data = response['data'];
                 var data2 = response['data2'];
                 // window.location.reload()

                 var color1 = Math.floor(Math.random() * 256);
                 var color2 = Math.floor(Math.random() * 256);
                 var color3 = Math.floor(Math.random() * 256);

                 var newlabel = data['x'];
                 console.log(color1 + " " + color2 + " " + color3)
                 var newDataset = {
                    label: "Count",
                    lineTension: 0.3,
                    backgroundColor: "rgba(78, 115, 223, 0.05)",
                    borderColor: "rgba(78, 115, 223, 1)",
                    pointRadius: 3,
                    pointBackgroundColor: "rgba(78, 115, 223, 1)",
                    pointBorderColor: "rgba(78, 115, 223, 1)",
                    pointHoverRadius: 3,
                    pointHoverBackgroundColor: "rgba(78, 115, 223, 1)",
                    pointHoverBorderColor: "rgba(78, 115, 223, 1)",
                    pointHitRadius: 10,
                    pointBorderWidth: 2,
                    data: data['y'],
                 }

                 // chart에 newDataset 푸쉬
                 lineConfig.data.datasets.push(newDataset);
                 // config.data.labels.pop();
                 lineConfig.data.labels = newlabel;

                 myLineChart.update();	//차트 업데이트

                 var newlabel2 = data2['labels'];
                 var newDataset2 = {
                  data: data2['per'],
                  backgroundColor: ['#4e73df', '#1cc88a', '#e74a3b', '#36b9cc', '#858796'],
                  hoverBackgroundColor: ['#4e73df', '#1cc88a', '#e74a3b', '#36b9cc', '#858796'],
                  hoverBorderColor: "rgba(234, 236, 244, 1)",
                }

                let temphtml = `<span class="mr-2">
                                    <i class="fas fa-circle text-primary"></i> ${data2['labels'][0]}
                                </span>
                                <span class="mr-2">
                                    <i class="fas fa-circle text-success"></i> ${data2['labels'][1]}
                                </span>
                                <span class="mr-2">
                                    <i class="fas fa-circle text-danger"></i> ${data2['labels'][2]}
                                </span>
                                <span class="mr-2">
                                    <i class="fas fa-circle text-info"></i> ${data2['labels'][3]}
                                </span>
                                <span class="mr-2">
                                    <i class="fas fa-circle text-secondary"></i> ${data2['labels'][4]}
                                </span>`
                $('#pieTag').append(temphtml)
                pieConfig.data.labels = newlabel2;
                pieConfig.data.datasets.push(newDataset2);
                myPieChart.update();
             },
         });
     });
});
// Area Chart Example
var ctx = document.getElementById("myAreaChart");
var lineConfig = {
    type: 'line',
    data: {
        labels: [0],
        datasets: [],
    },
    options: {
        maintainAspectRatio: false,
        layout: {
            padding: {
                left: 10,
                right: 25,
                top: 25,
                bottom: 0
            }
        },
    scales: {
        xAxes: [{
        time: {
        unit: 'date'
        },
        gridLines: {
        display: false,
        drawBorder: false
        },
        ticks: {
        maxTicksLimit: 7
        }
        }],
        yAxes: [{
        ticks: {
        maxTicksLimit: 5,
        padding: 10,
        // Include a dollar sign in the ticks
        // callback: function(value, index, values) {
        // return '$' + number_format(value);
        // }
        },
        gridLines: {
        color: "rgb(234, 236, 244)",
        zeroLineColor: "rgb(234, 236, 244)",
        drawBorder: false,
        borderDash: [2],
        zeroLineBorderDash: [2]
        }
        }],
    },
    legend: {
    display: false
    },
    tooltips: {
    backgroundColor: "rgb(255,255,255)",
    bodyFontColor: "#858796",
    titleMarginBottom: 10,
    titleFontColor: '#6e707e',
    titleFontSize: 14,
    borderColor: '#dddfeb',
    borderWidth: 1,
    xPadding: 15,
    yPadding: 15,
    displayColors: false,
    intersect: false,
    mode: 'index',
    caretPadding: 10,
    callbacks: {
    label: function(tooltipItem, chart) {
    var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
    return datasetLabel + ': $' + number_format(tooltipItem.yLabel);
    }
    }
    }
    }
    };
var myLineChart = new Chart(ctx, lineConfig);
