<script setup>

import { ref, reactive, onMounted } from "vue";
import api from "../services/api";


// ======================================================
// PROPS
// ======================================================

const props = defineProps({

    task: {

        type: Object,

        default: null,

    },

});


// ======================================================
// EMITS
// ======================================================

const emit = defineEmits([

    "close",

    "saved",

]);


// ======================================================
// ETAT
// ======================================================

const loading = ref(false);

const projects = ref([]);

const categories = ref([]);



// ======================================================
// FORMULAIRE
// ======================================================

const form = reactive({

    title: props.task?.title || "",

    description: props.task?.description || "",

    project: props.task?.project?.id || "",

    category: props.task?.category?.id || "",

    priority: props.task?.priority || "medium",

    status: props.task?.status || "todo",

    due_date: props.task?.due_date || "",

    due_time: props.task?.due_time || "",

    estimated_duration:
        props.task?.estimated_duration || 30,

    color:
        props.task?.color || "#3B82F6",

    is_favorite:
        props.task?.is_favorite || false,

});



// ======================================================
// CREATION PROJET
// ======================================================

const creatingProject = ref(false);

const newProject = reactive({

    name: "",

    description: "",

    color: "#6366F1",

    icon: "📁",

});



// ======================================================
// CREATION CATEGORIE
// ======================================================

const creatingCategory = ref(false);

const newCategory = reactive({

    name: "",

    color: "#8B5CF6",

    icon: "🏷️",

});



// ======================================================
// ERREURS
// ======================================================

const errors = reactive({

    title: "",

});



// ======================================================
// VALIDATION
// ======================================================

const validateForm = () => {


    errors.title = "";


    if (!form.title.trim()) {


        errors.title =
            "Le titre est obligatoire.";


        return false;


    }


    return true;


};



// ======================================================
// CHARGER PROJETS
// ======================================================

const loadProjects = async () => {


    try {


        const response = await api.get(
            "projects/"
        );


        projects.value = response.data;


    }


    catch(error){


        console.error(
            "Erreur projets :",
            error
        );


    }


};



// ======================================================
// CHARGER CATEGORIES
// ======================================================

const loadCategories = async () => {


    try {


        const response = await api.get(
            "categories/"
        );


        categories.value = response.data;


    }


    catch(error){


        console.error(
            "Erreur catégories :",
            error
        );


    }


};



// ======================================================
// CREER PROJET
// ======================================================

const createProject = async () => {


    const response = await api.post(

        "projects/",

        {

            name:newProject.name,

            description:newProject.description,

            color:newProject.color,

            icon:newProject.icon,

        }

    );


    await loadProjects();


    form.project = response.data.id;


    creatingProject.value = false;


    newProject.name = "";

};



// ======================================================
// CREER CATEGORIE
// ======================================================

const createCategory = async () => {


    const response = await api.post(

        "categories/",

        {


            name:newCategory.name,

            color:newCategory.color,

            icon:newCategory.icon,


        }

    );


    await loadCategories();


    form.category = response.data.id;


    creatingCategory.value = false;


    newCategory.name = "";


};



// ======================================================
// SAUVEGARDE TACHE
// ======================================================

const saveTask = async () => {


    if(!validateForm())

        return;



    loading.value = true;



    try {



        let projectId = form.project;

        let categoryId = form.category;



        if(projectId === "__new__"){


            await createProject();


            projectId = form.project;


        }



        if(categoryId === "__new__"){


            await createCategory();


            categoryId = form.category;


        }

        const taskData = {

            title: form.title,

            description: form.description,

            project_id: projectId || null,

            category_id: categoryId || null,

            priority: form.priority,

            status: form.status,

            due_date: form.due_date || null,

            due_time: form.due_time || null,

            estimated_duration: Number(form.estimated_duration),

            color: form.color,

            is_favorite: form.is_favorite,

};



        if(props.task){


            await api.patch(

                `tasks/${props.task.id}/`,

                taskData

            );


        }

        else{


            await api.post(

                "tasks/",

                taskData

            );


        }



        emit("saved");


        emit("close");



    }


    catch(error){


        console.error(

            error.response?.data || error

        );


    }


    finally{


        loading.value = false;


    }



};



// ======================================================
// DUREE
// ======================================================

const increaseDuration = () => {


    form.estimated_duration += 5;


};



const decreaseDuration = () => {


    if(form.estimated_duration > 5){


        form.estimated_duration -= 5;


    }


};



// ======================================================
// FERMER
// ======================================================

const closeForm = () => {


    emit("close");


};



// ======================================================
// INIT
// ======================================================

onMounted(async()=>{


    await Promise.all([

        loadProjects(),

        loadCategories(),

    ]);


});


</script>

<template>

<div class="overlay">

    <div class="task-modal">


        <!-- HEADER -->

        <div class="modal-header">


            <div>

                <h2>

                    {{ props.task ? "Modifier la tâche" : "Nouvelle tâche" }}

                </h2>


                <p>

                    Organisez votre travail efficacement.

                </p>


            </div>



            <button

                class="close-btn"

                @click="closeForm"

            >

                ✕

            </button>


        </div>



        <!-- INFORMATIONS -->

        <div class="section">


            <h3>
                📝 Informations
            </h3>



            <label>
                Titre *
            </label>


            <input

                v-model="form.title"

                placeholder="Nom de la tâche"

            />



            <small

                v-if="errors.title"

                class="error"

            >

                {{ errors.title }}

            </small>




            <label>
                Description
            </label>


            <textarea

                v-model="form.description"

                placeholder="Décrivez votre tâche..."

            />



        </div>





        <!-- ORGANISATION -->

        <div class="section">


            <h3>
                📁 Organisation
            </h3>



            <div class="grid">


                <!-- PROJET -->


                <div>


                    <label>
                        Projet
                    </label>



                    <select

                        v-model="form.project"

                    >


                        <option value="">

                            Sans projet

                        </option>



                        <option

                            v-for="project in projects"

                            :key="project.id"

                            :value="project.id"

                        >

                            {{ project.name }}

                        </option>



                        <option value="__new__">

                            ➕ Créer un projet

                        </option>



                    </select>



                </div>





                <!-- CATEGORIE -->

                <div>


                    <label>
                        Catégorie
                    </label>



                    <select

                        v-model="form.category"

                    >


                        <option value="">

                            Sans catégorie

                        </option>



                        <option

                            v-for="category in categories"

                            :key="category.id"

                            :value="category.id"

                        >

                            {{ category.name }}

                        </option>




                        <option value="__new__">

                            ➕ Créer une catégorie

                        </option>


                    </select>


                </div>



            </div>





            <!-- NOUVEAU PROJET -->


            <div

                v-if="form.project==='__new__'"

                class="create-box"

            >


                <h4>
                    Nouveau projet
                </h4>


                <input

                    v-model="newProject.name"

                    placeholder="Nom du projet"

                />



                <textarea

                    v-model="newProject.description"

                    placeholder="Description du projet"

                />



                <button

                    class="create-btn"

                    @click="createProject"

                >

                    Créer le projet

                </button>



            </div>







            <!-- NOUVELLE CATEGORIE -->


            <div

                v-if="form.category==='__new__'"

                class="create-box"

            >


                <h4>
                    Nouvelle catégorie
                </h4>



                <input

                    v-model="newCategory.name"

                    placeholder="Nom de la catégorie"

                />



                <button

                    class="create-btn"

                    @click="createCategory"

                >

                    Créer la catégorie

                </button>



            </div>




        </div>







        <!-- PRIORITE -->


        <div class="section">


            <h3>
                ⭐ Priorité
            </h3>


            <select

                v-model="form.priority"

            >


                <option value="low">
                    🟢 Faible
                </option>


                <option value="medium">
                    🟡 Moyenne
                </option>


                <option value="high">
                    🟠 Élevée
                </option>


                <option value="urgent">
                    🔴 Urgente
                </option>


            </select>



        </div>







        <!-- PLANIFICATION -->


        <div class="section">


            <h3>
                📅 Planification
            </h3>



            <div class="grid">


                <div>

                    <label>
                        Date limite
                    </label>


                    <input

                        type="date"

                        v-model="form.due_date"

                    />


                </div>



                <div>

                    <label>
                        Heure
                    </label>


                    <input

                        type="time"

                        v-model="form.due_time"

                    />


                </div>




            </div>





            <div class="duration">


                <label>
                    Durée estimée
                </label>


                <div class="counter">


                    <button

                        @click="decreaseDuration"

                    >

                        −

                    </button>



                    <span>

                        {{ form.estimated_duration }}

                        minutes

                    </span>



                    <button

                        @click="increaseDuration"

                    >

                        +

                    </button>



                </div>


            </div>




        </div>






        <!-- OPTIONS -->


        <div class="section">


            <h3>
                ⚙️ Options
            </h3>



            <label class="favorite">


                <input

                    type="checkbox"

                    v-model="form.is_favorite"

                />


                Ajouter aux favoris


            </label>



        </div>







        <!-- FOOTER -->


        <div class="footer">


            <button

                class="cancel"

                @click="closeForm"

            >

                Annuler

            </button>




            <button

                class="save"

                @click="saveTask"

                :disabled="loading"

            >

                {{loading ? "Enregistrement..." : "Enregistrer"}}


            </button>



        </div>



    </div>

</div>


</template>



<style scoped>

.overlay{

position:fixed;
inset:0;
background:rgba(15,23,42,.8);
display:flex;
align-items:center;
justify-content:center;
z-index:9999;

}



.task-modal{

width:min(950px,95%);

max-height:90vh;

overflow:auto;

background:#0f172a;

padding:32px;

border-radius:28px;

color:white;

box-shadow:0 30px 80px rgba(0,0,0,.5);

}



.modal-header{

display:flex;

justify-content:space-between;

margin-bottom:25px;

}



.close-btn{

background:#1e293b;

color:white;

border:none;

border-radius:12px;

width:42px;

height:42px;

cursor:pointer;

}



.section{

background:#1e293b;

padding:22px;

border-radius:20px;

margin-bottom:20px;

}



label{

display:block;

margin-bottom:8px;

color:#cbd5e1;

font-weight:600;

}



input,
textarea,
select{

width:100%;

padding:14px;

border-radius:14px;

border:none;

background:#172033;

color:white;

margin-bottom:15px;

}



textarea{

min-height:120px;

}



.grid{

display:grid;

grid-template-columns:1fr 1fr;

gap:20px;

}



.create-box{

margin-top:20px;

padding:20px;

background:#172033;

border-radius:18px;

border:1px solid #334155;

}



.create-btn{

background:#2563eb;

color:white;

border:none;

padding:12px 18px;

border-radius:12px;

cursor:pointer;

}



.duration{

margin-top:20px;

}



.counter{

display:flex;

align-items:center;

gap:20px;

}



.counter button{

width:40px;

height:40px;

border:none;

border-radius:10px;

background:#2563eb;

color:white;

font-size:22px;

cursor:pointer;

}



.favorite{

display:flex;

gap:10px;

align-items:center;

}



.footer{

display:flex;

justify-content:flex-end;

gap:15px;

}



.cancel,
.save{

padding:14px 25px;

border:none;

border-radius:14px;

cursor:pointer;

}



.cancel{

background:#334155;

color:white;

}



.save{

background:#2563eb;

color:white;

font-weight:700;

}



.error{

color:#ef4444;

}



@media(max-width:800px){

.grid{

grid-template-columns:1fr;

}


.footer{

flex-direction:column;

}


}


</style>