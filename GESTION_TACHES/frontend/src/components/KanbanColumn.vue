
<script setup>
import { computed } from "vue";
import TaskCard from "./TaskCard.vue";
const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  status: {
    type: String,
    required: true,
  },
  tasks: {
    type: Array,
    required: true,
  },
});
const emit = defineEmits([
  "taskMoved",
  "editTask",
  "deleteTask",
  "archiveTask",
]);
const columnTasks = computed(() => {
  return props.tasks.filter(
    (task) => task.status === props.status
  );
});
const handleDrop = (event) => {
  const taskId = event.dataTransfer.getData("taskId");
  if (taskId) {
    emit("taskMoved", {
      taskId: Number(taskId),
      newStatus: props.status,
    });
  }
};
const allowDrop = (event) => {
  event.preventDefault();
};
</script>
<template>
  <div
    class="kanban-column"
    @dragover="allowDrop"
    @drop="handleDrop"
  >
    <div class="column-header">
      <h3>{{ title }}</h3>
      <span>
        {{ columnTasks.length }}
      </span>
    </div>
    <div class="tasks-container">
      <TaskCard
        v-for="task in columnTasks"
        :key="task.id"
        :task="task"
        @editTask="emit('editTask', $event)"
        @deleteTask="emit('deleteTask', $event)"
        @archiveTask="emit('archiveTask', $event)"
      />
      <div
        v-if="columnTasks.length === 0"
        class="empty-column"
      >
        Déposer une tâche ici
      </div>
    </div>
  </div>
</template>
<style scoped>
.kanban-column {
  background: rgba(30, 41, 59, 0.7);
  border-radius: 18px;
  padding: 20px;
  min-height: 450px;
  transition: 0.3s;
}
.kanban-column:hover {
  transform: translateY(-3px);
}
.column-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 18px;
}
.column-header h3 {
  font-size: 18px;
  font-weight: 700;
  color: white;
}
.column-header span {
  background: #2563eb;
  color: white;
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 13px;
}
.tasks-container {
  display: flex;
  flex-direction: column;
  gap: 15px;
}
.empty-column {
  border: 2px dashed #64748b;
  padding: 25px;
  text-align: center;
  border-radius: 15px;
  color: #94a3b8;
}
</style>