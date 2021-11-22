import Vue from "vue";
import Router from "vue-router";
import Home from "@/views/Home"

Vue.use(Router)

export default new Router({
    mode: "history",
    routes: [
        {
            path: '/',
            component:Home
        },
        {
            path: '/movies',
            component: () => import("./views/MoviesPage")
        },
        {
            path: '/actors',
            component: () => import('./views/ActorsPage')
        },
        {
            path: '/directors',
            component: () => import('./views/DirectorsPage')
        }
    ]
})