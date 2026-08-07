<script setup>

import { ref, computed, onMounted } from "vue";
import api from "../services/api";


const tasks = ref([]);

const loading = ref(true);


const currentDate = ref(
    new Date()
);


// ===============================
// CHARGEMENT CALENDRIER
// ===============================

const loadCalendar = async () => {

    try {

        loading.value = true;

        const response = await api.get(
            "calendar/"
        );

        tasks.value = response.data;

    }

    catch(error){

        console.error(
            "Erreur calendrier :",
            error.response?.data || error
        );

    }

    finally{

        loading.value = false;

    }

};


// ===============================
// MOIS ACTUEL
// ===============================

const monthName = computed(()=>{

    return currentDate.value.toLocaleDateString(
        "fr-FR",
        {
            month:"long",
            year:"numeric"
        }
    );

});


// ===============================
// JOURS DU MOIS
// ===============================

const days = computed(()=>{

    const year =
        currentDate.value.getFullYear();

    const month =
        currentDate.value.getMonth();


    const firstDay =
        new Date(
            year,
            month,
            1
        );


    const lastDay =
        new Date(
            year,
            month + 1,
            0
        );


    const result = [];


    for(
        let i = 1;
        i <= lastDay.getDate();
        i++
    ){

        const date =
            new Date(
                year,
                month,
                i
            );


        result.push(date);

    }


    return result;

});


// ===============================
// TACHES D'UN JOUR
// ===============================

const getTasksForDay = (day)=>{


    const date =
        day.toISOString()
        .split("T")[0];


    return tasks.value.filter(
        task =>
            task.date === date
    );

};



// ===============================
// NAVIGATION
// ===============================

const previousMonth = ()=>{

    currentDate.value =
        new Date(
            currentDate.value.getFullYear(),
            currentDate.value.getMonth()-1,
            1
        );

};


const nextMonth = ()=>{

    currentDate.value =
        new Date(
            currentDate.value.getFullYear(),
            currentDate.value.getMonth()+1,
            1
        );

};



// ===============================
// COULEUR PRIORITE
// ===============================

const priorityClass = (priority)=>{


    return {

        low:"low",

        medium:"medium",

        high:"high",

        urgent:"urgent"

    }[priority] || "medium";


};



onMounted(()=>{

    loadCalendar();

});


</script>


<template>


<div class="calendar-page">


    <!-- HEADER -->

    <div class="calendar-header">


        <div>

            <h1>
                📅 Calendrier
            </h1>


            <p>
                Visualisez vos tâches et échéances.
            </p>

        </div>



        <div class="navigation">


            <button
                @click="previousMonth"
            >
                ◀
            </button>


            <h2>
                {{ monthName }}
            </h2>


            <button
                @click="nextMonth"
            >
                ▶
            </button>


        </div>


    </div>




    <!-- LOADING -->


    <div
        v-if="loading"
        class="loading"
    >

        Chargement du calendrier...

    </div>




    <!-- CALENDRIER -->


    <div
        v-else
        class="calendar-grid"
    >


        <div
            v-for="day in days"
            :key="day"
            class="day-card"
        >


            <div class="day-number">

                {{ day.getDate() }}

            </div>



            <div
                class="events"
            >


                <div

                    v-for="task in getTasksForDay(day)"

                    :key="task.id"

                    class="event"

                    :class="
                        priorityClass(task.priority)
                    "

                >

                    <strong>
                        {{ task.title }}
                    </strong>


                    <small>

                        {{ task.time || "Sans heure" }}

                    </small>


                    <small>

                        📁
                        {{ task.project || "Sans projet" }}

                    </small>


                </div>


            </div>


        </div>


    </div>


</div>


</template>

<style scoped>


.calendar-page{

    min-height:100vh;

    padding:32px;

    background:#0b2b77;

    color:white;

}


/* ===============================
   HEADER
================================ */

.calendar-header{

    display:flex;

    justify-content:space-between;

    align-items:center;

    margin-bottom:30px;

}


.calendar-header h1{

    font-size:32px;

    font-weight:800;

    margin:0;

}


.calendar-header p{

    color:#94a3b8;

    margin-top:8px;

}



/* ===============================
   NAVIGATION
================================ */


.navigation{

    display:flex;

    align-items:center;

    gap:20px;

}


.navigation h2{

    text-transform:capitalize;

    font-size:22px;

}


.navigation button{

    width:45px;

    height:45px;

    border:none;

    border-radius:14px;

    background:#2563eb;

    color:white;

    cursor:pointer;

    font-size:18px;

    transition:.25s;

}


.navigation button:hover{

    transform:translateY(-3px);

    background:#1d4ed8;

}



/* ===============================
   LOADING
================================ */


.loading{

    height:400px;

    display:flex;

    justify-content:center;

    align-items:center;

    font-size:18px;

    color:#cbd5e1;

}



/* ===============================
   CALENDRIER
================================ */


.calendar-grid{

    display:grid;

    grid-template-columns:
    repeat(7,1fr);

    gap:18px;

}



.day-card{

    min-height:150px;

    padding:16px;

    border-radius:20px;

    background:#1e293b;

    border:1px solid #334155;

    transition:.25s;

}


.day-card:hover{

    transform:translateY(-4px);

    box-shadow:
    0 15px 30px rgba(0,0,0,.35);

}



.day-number{

    width:35px;

    height:35px;

    display:flex;

    justify-content:center;

    align-items:center;

    border-radius:50%;

    background:#2563eb;

    font-weight:700;

    margin-bottom:15px;

}



/* ===============================
   EVENTS
================================ */


.events{

    display:flex;

    flex-direction:column;

    gap:10px;

}



.event{

    padding:12px;

    border-radius:14px;

    background:#0f172a;

    border-left:4px solid;

    display:flex;

    flex-direction:column;

    gap:5px;

    cursor:pointer;

    transition:.25s;

}



.event:hover{

    transform:translateX(5px);

}



.event strong{

    font-size:14px;

}



.event small{

    color:#cbd5e1;

    font-size:12px;

}



/* ===============================
   PRIORITES
================================ */


.event.low{

    border-color:#22c55e;

}


.event.medium{

    border-color:#f59e0b;

}


.event.high{

    border-color:#ef4444;

}


.event.urgent{

    border-color:#dc2626;

    background:#450a0a;

}



/* ===============================
   RESPONSIVE
================================ */


@media(max-width:1100px){


    .calendar-grid{

        grid-template-columns:
        repeat(4,1fr);

    }

}



@media(max-width:750px){


    .calendar-page{

        padding:18px;

    }


    .calendar-header{

        flex-direction:column;

        align-items:flex-start;

        gap:20px;

    }


    .calendar-grid{

        grid-template-columns:
        repeat(2,1fr);

    }

}



@media(max-width:450px){


    .calendar-grid{

        grid-template-columns:1fr;

    }


}



</style>