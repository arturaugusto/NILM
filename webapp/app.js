var app = new Vue({
  el: '#app',
  data: {
    loads: [
      {'name': 'Carga A', isOn: false},
      {'name': 'Carga B', isOn: false},
      {'name': 'Carga C', isOn: false}
    ],
    newName: '',
    state: undefined,
    chart: undefined,
    savedStates: [],
    prediction: []
  },
  methods: {
    train () {
      fetch('http://127.0.0.1:5000/trainState', {
        method: 'POST',
        cache: "no-cache",
        headers: {'Accept': 'application/json', 'Content-Type': 'application/json'},
        body: JSON.stringify(this.savedStates)
      }).then(res => {
        console.log(res)
      })


    },
    saveState () {
      if (!this.state) return
      this.savedStates.push({
        state: this.state,
        loads: this.loads.filter(item => item.isOn).map(item => item.name)
      })
    },
    newLoad () {
      if (!this.newName.length) return
      this.loads.push({'name': this.newName, isOn: false})
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

        // create chart
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
                //type: 'logarithmic',
                ticks: {
                  beginAtZero:true,
                  //max:1,
                  min: 0.001,
                  //autoSkip: true,
                  //autoSkipPadding: 0
                }
              }]
            }
          }
        })
        // update chart
        this.chart.data.labels = res.freq
        this.chart.data.datasets[0].data = res.mag
        this.chart.update()

        // set prediction
        this.prediction = res.prediction

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