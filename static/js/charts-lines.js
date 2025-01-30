/**
 * For usage, visit Chart.js docs https://www.chartjs.org/docs/latest/
 */
const lineConfig = {
  type: 'line',
  data: {
    labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
    datasets: [
      {
        label: 'Respuestas',
        /**
         * These colors come from Tailwind CSS palette
         * https://tailwindcss.com/docs/customizing-colors/#default-color-palette
         */
        backgroundColor: '#0694a2',
        borderColor: '#0694a2',
        data: [43, 48, 40, 54, 67, 73, 70],
        fill: false,
      },
      /**
      {
        label: 'Paid',
        fill: false,
        
         * These colors come from Tailwind CSS palette
         * https://tailwindcss.com/docs/customizing-colors/#default-color-palette
         
        backgroundColor: '#7e3af2',
        borderColor: '#7e3af2',
        data: [24, 50, 64, 74, 52, 51, 65],
      },*/
    ],
  },
  options: {
    responsive: true,
    /**
     * Default legends are ugly and impossible to style.
     * See examples in charts.html to add your own legends
     *  */
    legend: {
      display: false,
    },
    tooltips: {
      mode: 'index',
      intersect: false,
    },
    hover: {
      mode: 'nearest',
      intersect: true,
    },
    scales: {
      x: {
        display: true,
        scaleLabel: {
          display: true,
          labelString: 'Month',
        },
      },
      y: {
        display: true,
        scaleLabel: {
          display: true,
          labelString: 'Value',
        },
      },
    },
  },
}


// change this to the id of your chart element in HMTL
const lineCtx = document.getElementById('line')
window.myLine = new Chart(lineCtx, lineConfig)

// Función para procesar el JSON
countCommentsByDays = (data) => {
  
  // Crear un objeto para almacenar las frecuencias por fecha
  const valores = Object.values(data);
  const conteoFechas = {};

  // Función para convertir la fecha 'dd/mm/yyyy' a un objeto Date para ordenarla
  const convertirAFecha = (fecha) => {
    const [dia, mes, anio] = fecha.split('/');
    return new Date(anio, mes - 1, dia); // Recuerda que los meses en JavaScript son 0-indexados
  };

  // Procesar cada elemento de la lista
  valores.forEach((elemento) => {
    // Extraer solo la fecha (parte antes de la coma en 'saved')
    const fecha = elemento.saved.split(',')[0];

    // Incrementar el conteo para esa fecha
    if (conteoFechas[fecha]) {
      conteoFechas[fecha] += 1;
    } else {
      conteoFechas[fecha] = 1;
    }
  });

  // Ordenar las fechas (labels) de manera ascendente
  const labels = Object.keys(conteoFechas)
    .sort((a, b) => convertirAFecha(a) - convertirAFecha(b));

  const counts = labels.map((fecha) => conteoFechas[fecha]);

  return { labels, counts };
};

update = () => {
  fetch('/api/v1/landing')
    .then(response => response.json())
    .then(data => {

      let { labels, counts } = countCommentsByDays(data)

      // Reset data
      window.myLine.data.labels = [];
      window.myLine.data.datasets[0].data = [];
      

      // New data
      window.myLine.data.labels = [...labels]
      window.myLine.data.datasets[0].data = [...counts]

      window.myLine.update();

    })
    .catch(error => console.error('Error:', error));
}

update();