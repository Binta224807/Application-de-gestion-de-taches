<script setup>

import { computed } from "vue";
import { useRouter } from "vue-router";
import { formatDuration } from "../services/formatDuration.js";
import { User, Hourglass, CalendarDays } from "lucide-vue-next";

const props = defineProps({
  task: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits([
  "editTask",
  "deleteTask",
]);

const router = useRouter();

const priorityLabel = computed(() => {

  const labels = {
    low: "Faible",
    medium: "Moyenne",
    high: "Élevée",
    urgent: "Urgente",
  };

  return labels[props.task.priority] || props.task.priority;

});

const statusLabel = computed(() => {

  const labels = {
    todo: "À faire",
    in_progress: "En cours",
    review: "À vérifier",
    done: "Terminée",
  };

  return labels[props.task.status] || props.task.status;

});

const assignedName = computed(() => {

  const assignees = props.task.assigned_to || [];

  if (!assignees.length) {

    return "Non assigné";

  }

  const names = assignees
    .map((u) => u.username);

  if (names.length === 1) {

    return names[0];

  }

  return `${names[0]} +${names.length - 1}`;

});

const goToDetail = () => {

  router.push(`/tasks/${props.task.id}`);

};

const editTask = () => {

  emit("editTask", props.task);

};

const deleteTask = () => {

  emit("deleteTask", props.task);

};

</script>


<template>

  <div class="task-row">

    <!-- COLONNE GAUCHE : TITRE + DESCRIPTION -->

    <div class="task-main">

      <h3 class="task-title">
        {{ task.title }}
      </h3>

      <p class="task-description">
        {{ task.description || "Aucune description" }}
      </p>

    </div>


    <!-- COLONNE CENTRALE : INFOS -->

    <div class="task-meta">

      <span
        class="badge status-badge"
        :class="task.status"
      >
        {{ statusLabel }}
      </span>

      <span
        class="badge priority-badge"
        :class="task.priority"
      >
        {{ priorityLabel }}
      </span>

      <span class="meta-item">
        <User :size="13" /> {{ assignedName }}
      </span>

      <span class="meta-item">
        <Hourglass :size="13" /> {{ formatDuration(task.estimated_duration) }}
      </span>

      <span
        v-if="task.due_date"
        class="meta-item"
      >
        <CalendarDays :size="13" /> {{ task.due_date }}
      </span>

    </div>


    <!-- COLONNE DROITE : ACTION -->

    <div class="task-actions">

      <button
        class="btn-detail"
        @click="goToDetail"
      >
        Détails
      </button>

    </div>

  </div>

</template>


<style scoped>

.task-row {

  width: 100%;
  box-sizing: border-box;

  background: #111827;

  border: 1px solid rgba(255, 255, 255, 0.08);

  border-radius: 16px;

  padding: 18px 20px;

  display: grid;
  grid-template-columns: 1fr auto auto;
  align-items: center;
  gap: 20px;

  transition: .25s;

  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);

}


.task-row:hover {

  border-color: #2563eb;

  box-shadow: 0 8px 24px rgba(37, 99, 235, 0.2);

  transform: translateY(-2px);

}


.task-main {

  min-width: 0;

  overflow: hidden;

}


.task-title {

  font-size: 17px;
  font-weight: 700;
  color: white;
  margin: 0 0 6px 0;

  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;

}


.task-description {

  color: #94a3b8;
  font-size: 13px;
  margin: 0;

  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;

}


.task-meta {

  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;

}


.badge {

  padding: 5px 10px;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  color: white;

}


.priority-badge.low {
  background: #22c55e;
}

.priority-badge.medium {
  background: #f59e0b;
}

.priority-badge.high {
  background: #ef4444;
}

.priority-badge.urgent {
  background: #dc2626;
}


.status-badge.todo {
  background: #3b82f6;
}

.status-badge.in_progress {
  background: #d97706;
}

.status-badge.review {
  background: #8b5cf6;
}

.status-badge.done {
  background: #16a34a;
}


.meta-item {

  color: var(--text-strong);
  font-size: 13px;
  padding: 4px 10px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;

  white-space: nowrap;

  display: inline-flex;
  align-items: center;
  gap: 6px;

}


.task-actions {

  display: flex;
  align-items: center;
  gap: 8px;

}


.btn-detail {

  background: #2563eb;
  color: white;
  border: none;
  border-radius: 10px;
  padding: 10px 18px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: .2s;

  white-space: nowrap;

}


.btn-detail:hover {

  background: #1d4ed8;
  transform: translateY(-1px);

}


/* TABLETTE */

@media (max-width: 1024px) {

  .task-row {

    grid-template-columns: 1fr auto;
    gap: 16px;

  }

  .task-actions {

    grid-column: 2;
    grid-row: 1;

  }

  .task-meta {

    grid-column: 1 / -1;
    justify-content: flex-start;

  }

}


/* MOBILE */

@media (max-width: 640px) {

  .task-row {

    grid-template-columns: 1fr;
    gap: 14px;
    padding: 16px;

  }

  .task-title {

    font-size: 16px;
    white-space: normal;

  }

  .task-description {

    white-space: normal;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;

  }

  .task-meta {

    flex-wrap: wrap;
    gap: 8px;

  }

  .task-actions {

    width: 100%;

  }

  .btn-detail {

    width: 100%;
    padding: 12px;
    font-size: 14px;

  }

}

</style>
