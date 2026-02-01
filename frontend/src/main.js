import { createPinia } from 'pinia'
import { createApp } from 'vue'
import {
  Quasar,
  Notify,
  Dialog,
  QLayout,
  QHeader,
  QDrawer,
  QList,
  QItem,
  QItemSection,
  QItemLabel,
  QToolbar,
  QToolbarTitle,
  QPageContainer,
  QPage,
  QBtn,
  QDialog,
  QCard,
  QCardSection,
  QCardActions,
  QTable,
  QTd,
  QInnerLoading,
  QInput,
  QIcon,
  QSelect,
  QBadge,
  QSpace,
  QTabs,
  QTab,
  QTabPanels,
  QTabPanel,
  QToggle,
  QChip,
  QTree,
  QExpansionItem,
  QFile,
  QSpinner,
  QLinearProgress,
  QTooltip
} from 'quasar'
import '@quasar/extras/roboto-font/roboto-font.css'
import '@quasar/extras/material-icons/material-icons.css'
import 'quasar/dist/quasar.css'
import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(Quasar, {
  plugins: {
    Notify,
    Dialog
  },
  components: {
    QLayout,
    QHeader,
    QDrawer,
    QList,
    QItem,
    QItemSection,
    QItemLabel,
    QToolbar,
    QToolbarTitle,
    QPageContainer,
    QPage,
    QBtn,
    QDialog,
    QCard,
    QCardSection,
    QCardActions,
    QTable,
    QTd,
    QInnerLoading,
    QInput,
    QIcon,
    QSelect,
    QBadge,
    QSpace,
    QTabs,
    QTab,
    QTabPanels,
    QTabPanel,
    QToggle,
    QChip,
    QTree,
    QExpansionItem,
    QFile,
    QSpinner,
    QLinearProgress,
    QTooltip
  },
  config: {
    dark: false,
    notify: {
      position: 'top',
      timeout: 2500
    }
  }
})

app.mount('#app')
