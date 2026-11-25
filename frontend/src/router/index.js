import { createRouter, createWebHistory } from "vue-router";

import Login from "../views/Login.vue";
import Register from "../views/Register.vue";

import Calendar from "../pages/Calendar.vue";
import Statistics from "../pages/Statistics.vue";
import Archives from "../pages/Archives.vue";
import TaskDetail from "../pages/TaskDetail.vue";
import Company from "../pages/Company.vue";
import Notifications from "../pages/Notifications.vue";

import TableauDeBord from "../pages/TableauDeBord.vue";
import Kanban from "../pages/kanban.vue";
import Projects from "../pages/Projects.vue";
import ProjectDetail from "../pages/ProjectDetail.vue";


const routes = [

  {
    path: "/",
    redirect: "/login"
  },

  {
    path: "/login",
    name: "Login",
    component: Login
  },

  {
    path: "/register",
    name: "Register",
    component: Register
  },

  {
    path: "/dashboard",
    name: "Dashboard",
    component: TableauDeBord,
    meta: {
      requiresAuth: true
    }
  },

  {
    path: "/tasks",
    name: "Tasks",
    component: Kanban,
    meta: {
      requiresAuth: true
    }
  },

  {
    path: "/tasks/:id",
    name: "TaskDetail",
    component: TaskDetail,
    meta: {
      requiresAuth: true
    }
  },

  {
    path: "/projects",
    name: "Projects",
    component: Projects,
    meta: {
      requiresAuth: true
    }
  },

  {
    path: "/projects/:id",
    name: "ProjectDetail",
    component: ProjectDetail,
    meta: {
      requiresAuth: true
    }
  },

  {
    path: "/calendar",
    name: "Calendar",
    component: Calendar,
    meta: {
      requiresAuth: true
    }
  },

  {
    path: "/statistics",
    name: "Statistics",
    component: Statistics,
    meta: {
      requiresAuth: true
    }
  },

  {
    path: "/archives",
    name: "Archives",
    component: Archives,
    meta: {
      requiresAuth: true
    }
  },

  {
    path: "/company",
    name: "Company",
    component: Company,
    meta: {
      requiresAuth: true,
      requiresCEO: true
    }
  },

  {
    path: "/notifications",
    name: "Notifications",
    component: Notifications,
    meta: {
      requiresAuth: true
    }
  }

];


const router = createRouter({
  history: createWebHistory(),
  routes
});


// Protection des pages
router.beforeEach((to, from, next) => {

  const token = localStorage.getItem("access") || localStorage.getItem("access_token");

  const isCEO = localStorage.getItem("is_ceo") === "1";

  if (to.meta.requiresAuth && !token) {
    next("/login");
  }

  else if (to.meta.requiresCEO && !isCEO) {
    next("/dashboard");
  }

  else if (to.path === "/login" && token) {
    next("/dashboard");
  }

  else if (to.path === "/kanban") {
    next("/tasks");
  }

  else {
    next();
  }

});


export default router;
