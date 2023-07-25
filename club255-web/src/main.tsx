import { createApp } from "vue";
import router from "./router.ts";

const app = createApp(() => <router-view></router-view>);
app.use(router);
app.mount("#app");
