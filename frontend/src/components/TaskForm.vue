<script setup>

import { ref, reactive, onMounted, computed } from "vue";
import api from "../services/api";
import { formatDuration } from "../services/formatDuration.js";
import {
    FileText,
    FolderKanban,
    Users,
    Flag,
    CalendarDays,
    Settings2,
    Check,
    X,
} from "lucide-vue-next";


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

const employees = ref([]);

const isCEO = ref(localStorage.getItem("is_ceo") === "1");



// ======================================================
// FORMULAIRE
// ======================================================

const form = reactive({

    title: props.task?.title || "",

    description: props.task?.description || "",

    project: props.task?.project?.id || "",

    category: props.task?.category?.id || "",

    assigned_to_ids: (props.task?.assigned_to || [])
        .map((u) => u.id),

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
// ASSIGNATION MULTIPLE
// ======================================================

const toggleAssignee = (employeeId) => {

    const index =
        form.assigned_to_ids.indexOf(employeeId);

    if (index === -1) {

        form.assigned_to_ids.push(employeeId);

    }

    else {

        form.assigned_to_ids.splice(index, 1);

    }

};


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

            assigned_to_ids: form.assigned_to_ids,

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

const loadEmployees = async () => {

    if (!isCEO.value) return;

    try {

        const response = await api.get("employees/");

        employees.value = response.data;

    }

    catch (error) {

        console.error("Erreur employés :", error);

    }

};


onMounted(async()=>{


    await Promise.all([

        loadProjects(),

        loadCategories(),

        loadEmployees(),

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

                <X :size="18" />

            </button>


        </div>



        <!-- INFORMATIONS -->

        <div class="section">


            <h3>
                <FileText :size="18" class="section-icon" /> Informations
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
                <FolderKanban :size="18" class="section-icon" /> Organisation
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

                            + Créer un projet

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

                            + Créer une catégorie

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







        <!-- ASSIGNATION -->

        <div
            v-if="isCEO"
            class="section"
        >

            <h3>
                <Users :size="18" class="section-icon" /> Assignation
            </h3>

            <label>
                Employés assignés
            </label>

            <div
                v-if="employees.length"
                class="assignees"
            >

                <button
                    v-for="employee in employees"
                    :key="employee.id"
                    type="button"
                    class="assignee-chip"
                    :class="{
                        selected: form.assigned_to_ids.includes(employee.id)
                    }"
                    @click="toggleAssignee(employee.id)"
                >

                    <span class="chip-avatar">
                        {{ employee.username.charAt(0).toUpperCase() }}
                    </span>

                    <span class="chip-name">
                        {{ employee.username }}
                    </span>

                    <Check
                        v-if="form.assigned_to_ids.includes(employee.id)"
                        :size="15"
                        class="chip-check"
                    />

                </button>

            </div>

            <p
                v-else
                class="no-employees"
            >
                Aucun employé dans l'entreprise.
            </p>

        </div>


        <!-- PRIORITE -->


        <div class="section">


            <h3>
                <Flag :size="18" class="section-icon" /> Priorité
            </h3>


            <select

                v-model="form.priority"

            >


                <option value="low">
                    Faible
                </option>


                <option value="medium">
                    Moyenne
                </option>


                <option value="high">
                    Élevée
                </option>


                <option value="urgent">
                    Urgente
                </option>


            </select>



        </div>







        <!-- PLANIFICATION -->


        <div class="section">


            <h3>
                <CalendarDays :size="18" class="section-icon" /> Planification
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

                        {{ formatDuration(form.estimated_duration) }}

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
                <Settings2 :size="18" class="section-icon" /> Options
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

.overlay {
    position: fixed;
    inset: 0;
    background: rgba(5, 7, 13, 0.8);
    backdrop-filter: blur(6px);

    display: flex;
    align-items: center;
    justify-content: center;

    z-index: 9999;

    padding: 20px;
}


/* =========================================
   MODALE
========================================= */

.task-modal {

    width: min(950px, 100%);

    max-height: 90vh;

    overflow-y: auto;

    background: #0f172a;

    padding: 32px;

    border-radius: 28px;

    color: white;

    box-shadow:
        0 30px 80px rgba(0, 0, 0, .5);
}


/* =========================================
   HEADER
========================================= */

.modal-header {

    display: flex;

    justify-content: space-between;

    align-items: flex-start;

    gap: 20px;

    margin-bottom: 25px;
}


.modal-header h2 {

    font-size: 24px;

    font-weight: 800;

    margin: 0;

}


.modal-header p {

    color: #94a3b8;

    margin-top: 6px;

}


.close-btn {

    flex-shrink: 0;

    background: #1e293b;

    color: white;

    border: none;

    border-radius: 12px;

    width: 42px;

    height: 42px;

    cursor: pointer;

    font-size: 18px;
}


/* =========================================
   SECTIONS
========================================= */

.section {

    background: #1e293b;

    padding: 22px;

    border-radius: 20px;

    margin-bottom: 20px;
}


.section h3 {

    margin-top: 0;

    margin-bottom: 18px;

    color: var(--text-h);

    display: flex;

    align-items: center;

    gap: 10px;

}


.section-icon {

    color: var(--accent);

    flex-shrink: 0;

}


/* =========================================
   ASSIGNATION
========================================= */

.assignees {

    display: flex;

    flex-wrap: wrap;

    gap: 10px;

    margin-bottom: 15px;

}


.assignee-chip {

    display: inline-flex;

    align-items: center;

    gap: 9px;

    padding: 8px 14px 8px 8px;

    border-radius: 999px;

    border: 1px solid var(--border-strong);

    background: var(--surface-2);

    color: var(--text);

    font-size: 14px;

    font-weight: 500;

    cursor: pointer;

    transition: .2s;

}


.assignee-chip:hover {

    border-color: var(--accent);

    color: var(--text-h);

    transform: translateY(-1px);

}


.assignee-chip.selected {

    animation: scale-in .25s ease;

}


.assignee-chip.selected {

    background: var(--accent-soft);

    border-color: var(--accent-border);

    color: var(--text-h);

}


.chip-avatar {

    width: 28px;

    height: 28px;

    border-radius: 50%;

    display: flex;

    align-items: center;

    justify-content: center;

    background: var(--accent-strong);

    color: white;

    font-size: 12px;

    font-weight: 700;

    flex-shrink: 0;

}


.chip-check {

    color: var(--accent);

    flex-shrink: 0;

}


.no-employees {

    color: var(--text);

    font-size: 14px;

}


/* =========================================
   FORM
========================================= */

label {

    display: block;

    margin-bottom: 8px;

    color: #cbd5e1;

    font-weight: 600;
}


input,
textarea,
select {

    width: 100%;

    box-sizing: border-box;

    padding: 14px;

    border-radius: 14px;

    border: 1px solid transparent;

    background: #172033;

    color: white;

    margin-bottom: 15px;

    font-size: 15px;
}


input:focus,
textarea:focus,
select:focus {

    outline: none;

    border-color: #2563eb;
}


textarea {

    min-height: 120px;

    resize: vertical;
}


/* =========================================
   GRILLE
========================================= */

.grid {

    display: grid;

    grid-template-columns: 1fr 1fr;

    gap: 20px;
}


/* =========================================
   CREATION
========================================= */

.create-box {

    margin-top: 20px;

    padding: 20px;

    background: #172033;

    border-radius: 18px;

    border: 1px solid #334155;
}


.create-btn {

    background: #2563eb;

    color: white;

    border: none;

    padding: 12px 18px;

    border-radius: 12px;

    cursor: pointer;

    font-weight: 600;
}


/* =========================================
   DUREE
========================================= */

.duration {

    margin-top: 20px;
}


.counter {

    display: flex;

    align-items: center;

    justify-content: center;

    gap: 20px;
}


.counter button {

    width: 44px;

    height: 44px;

    border: none;

    border-radius: 10px;

    background: #2563eb;

    color: white;

    font-size: 22px;

    cursor: pointer;
}


/* =========================================
   FAVORIS
========================================= */

.favorite {

    display: flex;

    align-items: center;

    gap: 10px;

    cursor: pointer;
}


.favorite input {

    width: auto;

    margin: 0;
}


/* =========================================
   FOOTER
========================================= */

.footer {

    display: flex;

    justify-content: flex-end;

    gap: 15px;

    margin-top: 10px;
}


.cancel,
.save {

    padding: 14px 25px;

    border: none;

    border-radius: 14px;

    cursor: pointer;

    font-weight: 700;
}


.cancel {

    background: #334155;

    color: white;
}


.save {

    background: #2563eb;

    color: white;
}


.save:disabled {

    opacity: .6;

    cursor: not-allowed;
}


.error {

    display: block;

    color: #ef4444;

    margin-top: -8px;

    margin-bottom: 12px;
}


/* =========================================
   TABLETTE
========================================= */

@media (max-width: 800px) {

    .grid {

        grid-template-columns: 1fr;
    }

}


/* =========================================
   MOBILE
========================================= */

@media (max-width: 600px) {

    .overlay {

        padding: 0;

        align-items: stretch;

    }


    .task-modal {

        width: 100%;

        max-height: 100dvh;

        height: 100dvh;

        border-radius: 0;

        padding: 20px 16px;

        padding-bottom: max(20px, env(safe-area-inset-bottom));

        overflow-y: auto;

        -webkit-overflow-scrolling: touch;

        box-sizing: border-box;
    }


    .modal-header {

        position: sticky;

        top: 0;

        z-index: 2;

        background: #0f172a;

        padding-bottom: 15px;

        margin-bottom: 15px;
    }


    .modal-header h2 {

        font-size: 21px;

    }


    .modal-header p {

        font-size: 13px;

    }


    .section {

        padding: 16px;

        border-radius: 16px;

        margin-bottom: 14px;
    }


    .section h3 {

        font-size: 16px;

    }


    input,
    textarea,
    select {

        font-size: 16px;

        padding: 13px;

    }


    textarea {

        min-height: 100px;

    }


    .footer {

        position: sticky;

        bottom: 0;

        background: #0f172a;

        padding: 15px 0 5px;

        flex-direction: column-reverse;

        gap: 10px;
    }


    .cancel,
    .save {

        width: 100%;

        min-height: 48px;

    }


    .counter {

        justify-content: space-between;

    }


    .counter button {

        width: 48px;

        height: 48px;

    }

}


/* =========================================
   PETIT TELEPHONE
========================================= */

@media (max-width: 380px) {

    .task-modal {

        padding: 16px 12px;

    }


    .section {

        padding: 14px;

    }


    .modal-header h2 {

        font-size: 19px;

    }

}

</style>