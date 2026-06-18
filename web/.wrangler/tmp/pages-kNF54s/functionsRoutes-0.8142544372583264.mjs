import { onRequest as __api__route__js_onRequest } from "A:\\卓面\\work\\CSDNExporter\\web\\functions\\api\\[route].js"

export const routes = [
    {
      routePath: "/api/:route",
      mountPath: "/api",
      method: "",
      middlewares: [],
      modules: [__api__route__js_onRequest],
    },
  ]