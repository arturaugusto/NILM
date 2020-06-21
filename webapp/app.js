var app = new Vue({
  el: '#app',
  data: {
    loads: [],
    newName: '',
    state: undefined,
    chart: undefined
  },
  methods: {
    newLoad () {
      if (!this.newName.length) return
      this.loads.push({'name': this.newName, state: false})
      this.newName = ''
    },
    getSpectrum () {
      fetch('http://127.0.0.1:5000/spectrum', {
        method: 'GET',
        cache: "no-cache",
        headers: {'Accept': 'application/json', 'Content-Type': 'application/json'},
        //body: JSON.stringify([{label: 'aaa', roi: [0,0,250,200]}])
        //body: JSON.stringify(monitor.regioes)
      })
      .then(res => res.json())
      .then(res => {
        this.state = res
        let ctx = this.$refs.spectrum
        console.log(res)
        this.chart = this.chart || new Chart(ctx, {
          type: 'bar',
          data: {
            labels: [],
            datasets: [{
              label: 'Spectrum',
              data: [],
              backgroundColor: 'rgba(255, 99, 132, 1)'
            }]
          },
          options: {
            scales: {
              xAxes: [{
                display: false,
                ticks: {}
              },
              {
                display: true
              }],
              yAxes: [{
                ticks: {
                  beginAtZero:true
                }
              }]
            }
          }
        })

        this.chart.data.labels = res[0]
        this.chart.data.datasets[0].data = res[1]
        this.chart.update()

      }).catch(err => {
        //..
      }).finally(_ => {
        window.setTimeout(this.getSpectrum, 1000)
      })
    }

  },
  mounted () {
    this.getSpectrum()
  }
})