<template>
  <div>

    <div
      v-if="tasks.length === 0"
      class="empty-state"
    >
      Aucune tâche.
    </div>

    <div
      v-for="task in tasks"
      :key="task.id"
      class="task-card"
    >

      <div class="task-header">

        <h3>{{ task.title }}</h3>

        <span
          class="priority"
          :class="task.priority"
        >
          {{ task.priority }}
        </span>

      </div>

      <p
        v-if="task.description"
        class="description"
      >
        {{ task.description }}
      </p>

      <div class="task-footer">

        <span>
          📅 {{ task.due_date || "Aucune date" }}
        </span>

        <span>
          📁 {{ task.project?.name || "Sans projet" }}
        </span>

      </div>

    </div>

  </div>
</template>

<script setup>

defineProps({

  tasks: {
    type: Array,
    default: () => []
  }

});

</script>

<style scoped>

.empty-state{

  text-align:center;

  color:#94a3b8;

  padding:20px;

}

.task-card{

  background:#0f172a;

  border:1px solid #334155;

  border-radius:16px;

  padding:16px;

  margin-bottom:14px;

}

.task-header{

  display:flex;

  justify-content:space-between;

  align-items:center;

}

.task-header h3{

  color:white;

  font-size:16px;

  font-weight:700;

}

.description{

  color:#cbd5e1;

  margin:12px 0;

}

.task-footer{

  display:flex;

  justify-content:space-between;

  color:#94a3b8;

  font-size:13px;

}

.priority{

  padding:4px 10px;

  border-radius:999px;

  font-size:12px;

  font-weight:700;

  text-transform:capitalize;

}

.priority.low{

  background:#22c55e33;

  color:#22c55e;

}

.priority.medium{

  background:#facc1533;

  color:#facc15;

}

.priority.high{

  background:#fb923c33;

  color:#fb923c;

}

.priority.urgent{

  background:#ef444433;

  color:#ef4444;

}

</style>