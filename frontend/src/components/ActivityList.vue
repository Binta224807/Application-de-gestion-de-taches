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

        <span class="meta">
          <CalendarDays :size="14" />
          {{ task.due_date || "Aucune date" }}
        </span>

        <span class="meta">
          <Folder :size="14" />
          {{ task.project?.name || "Sans projet" }}
        </span>

      </div>

    </div>

  </div>
</template>

<script setup>

import { CalendarDays, Folder } from "lucide-vue-next";

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

  color:var(--text);

  padding:20px;

}

.task-card{

  background:var(--surface-2);

  border:1px solid var(--border);

  border-radius:var(--radius);

  padding:16px;

  margin-bottom:14px;

  transition:border-color .2s;

}

.task-card:hover{

  border-color:var(--border-strong);

}

.task-header{

  display:flex;

  justify-content:space-between;

  align-items:center;

  gap:12px;

}

.task-header h3{

  color:var(--text-h);

  font-size:15px;

  font-weight:600;

}

.description{

  color:var(--text-strong);

  margin:12px 0;

  font-size:14px;

}

.task-footer{

  display:flex;

  justify-content:space-between;

  gap:12px;

  color:var(--text);

  font-size:13px;

}

.meta{

  display:inline-flex;

  align-items:center;

  gap:6px;

  min-width:0;

}

.priority{

  padding:4px 10px;

  border-radius:999px;

  font-size:11px;

  font-weight:600;

  text-transform:capitalize;

  flex-shrink:0;

}

.priority.low{

  background:#22c55e1f;

  color:#22c55e;

}

.priority.medium{

  background:#facc151f;

  color:#facc15;

}

.priority.high{

  background:#fb923c1f;

  color:#fb923c;

}

.priority.urgent{

  background:#ef44441f;

  color:#ef4444;

}

</style>
