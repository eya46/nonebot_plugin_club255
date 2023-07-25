import { createRouter, createWebHashHistory } from "vue-router";

export default createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      path: "/",
      component: () => import("./Show.vue"),
    },
    {
      path: "/hello",
      component: () => import("./views/HelloWorld.vue"),
    },
  ],
});
