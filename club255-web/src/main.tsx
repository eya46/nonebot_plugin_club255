import { createApp } from "vue";
import router from "./router.ts";

const app = createApp(() => {
  return <router-view></router-view>;
});
app.use(router);
app.mount("#app");
