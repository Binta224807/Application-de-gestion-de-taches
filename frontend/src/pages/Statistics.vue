<script setup>

import { ref, computed, onMounted } from "vue";
import api from "../services/api";

import {
    Chart as ChartJS,
    ArcElement,
    Tooltip,
    Legend,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    PointElement,
    LineElement
} from "chart.js";

import {
    Doughnut,
    Bar,
    Line
} from "vue-chartjs";


// ===============================
// CHART CONFIGURATION
// ===============================

ChartJS.register(
    ArcElement,
    Tooltip,
    Legend,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    PointElement,
    LineElement
);


// ===============================
// DATA
// ===============================

const tasks = ref([]);

const loading = ref(true);


// ===============================
// LOAD TASKS
// ===============================

const loadTasks = async () => {

    try {

        const response = await api.get(
            "tasks/"
        );

        tasks.value = response.data;

    }

    catch(error){

        console.error(error);

    }

    finally{

        loading.value = false;

    }

};


// ===============================
// STATISTIQUES
// ===============================


const statusData = computed(()=>({

    labels:[
        "À faire",
        "En cours",
        "Terminées"
    ],

    datasets:[
        {
            data:[

                tasks.value.filter(
                    t=>t.status==="todo"
                ).length,


                tasks.value.filter(
                    t=>t.status==="in_progress"
                ).length,


                tasks.value.filter(
                    t=>t.status==="done"
                ).length

            ],

            backgroundColor:[

                "#3B82F6",
                "#F59E0B",
                "#22C55E"

            ]

        }
    ]

}));



const priorityData = computed(()=>({

    labels:[

        "Faible",
        "Moyenne",
        "Élevée",
        "Urgente"

    ],

    datasets:[

        {

            label:"Nombre de tâches",

            data:[

                tasks.value.filter(
                    t=>t.priority==="low"
                ).length,


                tasks.value.filter(
                    t=>t.priority==="medium"
                ).length,


                tasks.value.filter(
                    t=>t.priority==="high"
                ).length,


                tasks.value.filter(
                    t=>t.priority==="urgent"
                ).length

            ]

        }

    ]

}));



// ===============================
// PROGRESSION
// ===============================

const progress = computed(()=>{


    if(tasks.value.length===0)

        return 0;


    return Math.round(

        (
            tasks.value.filter(
                t=>t.status==="done"
            ).length
            /
            tasks.value.length

        )*100

    );


});



// ===============================
// EVOLUTION
// ===============================


const evolutionData = computed(()=>({

    labels:[

        "Jan",
        "Fév",
        "Mar",
        "Avr",
        "Mai",
        "Juin"

    ],

    datasets:[

        {

            label:"Tâches créées",

            data:[

                5,
                10,
                7,
                15,
                12,
                tasks.value.length

            ],

            tension:0.4

        }

    ]

}));



onMounted(()=>{

    loadTasks();

});


</script>



<template>


<div class="statistics-page">


<h1>

📊 Statistiques

</h1>



<div v-if="loading">

Chargement...

</div>



<div v-else class="charts">



<div class="chart-card">

<h3>

Répartition des tâches

</h3>


<Doughnut

:data="statusData"

/>


</div>




<div class="chart-card">


<h3>

Priorités

</h3>


<Bar

:data="priorityData"

/>


</div>




<div class="chart-card full">


<h3>

Evolution des tâches

</h3>


<Line

:data="evolutionData"

/>


</div>




<div class="progress-card">


<h3>

Progression globale

</h3>


<div class="circle">


{{progress}}%


</div>


</div>



</div>


</div>


</template>



<style scoped>

.statistics-page{

    min: height 80px;

    padding:40px;

    background:
        radial-gradient(circle at top,#2b3f89 0%,#020617 55%);

}

.statistics-header{

    margin-bottom:40px;

}

.statistics-header h1{

    color:white;

    font-size:42px;

    font-weight:800;

}

.statistics-header p{

    color:#6191d3;

    margin-top:8px;

}

.loading{

    color:white;

    text-align:center;

    padding:60px;

}

.charts-grid{

    display:grid;

    grid-template-columns:repeat(2,1fr);

    gap:30px;

}

.chart-card{

    background:rgba(50, 81, 155, 0.72);

    backdrop-filter:blur(18px);

    border:1px solid hsla(198, 80%, 41%, 0.368);

    border-radius:26px;

    padding:60px;

    transition:.35s;

}

.chart-card:hover{

    transform:translateY(-8px);

    border-color:#3B82F6;

    box-shadow:0 20px 45px rgba(12, 35, 87, 0.35);

}

.chart-card h3{

    color:white;

    margin-bottom:20px;

    font-size:18px;

}

.chart-card canvas{

    width:100%!important;

    height:300px!important;

}

@media(max-width:800px){

    .charts-grid{

        grid-template-columns:1fr;

    }

}

</style>