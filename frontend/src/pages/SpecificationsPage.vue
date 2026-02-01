<template>
  <q-layout view="hHh Lpr fFf">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-btn flat dense round icon="arrow_back" @click="$router.push('/')" />
        <q-toolbar-title>File Specifications</q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      :width="300"
      :breakpoint="500"
      bordered
    >
      <q-list>
        <q-item-label header>Specifications</q-item-label>

        <q-expansion-item
          expand-separator
          icon="description"
          label="Input File Specification"
          default-opened
        >
          <q-list padding>
            <q-item 
              clickable 
              :active="selectedDoc === 'spec-readme'"
              @click="loadDoc('Input_File_Specification/README.md', 'spec-readme')"
              active-class="bg-blue-1"
            >
              <q-item-section>
                <q-item-label>Overview</q-item-label>
              </q-item-section>
            </q-item>

            <q-item 
              clickable 
              :active="selectedDoc === 'global-rules'"
              @click="loadDoc('Input_File_Specification/global_parsing_rules.md', 'global-rules')"
              active-class="bg-blue-1"
            >
              <q-item-section>
                <q-item-label>Global Parsing Rules</q-item-label>
              </q-item-section>
            </q-item>

            <q-separator spaced />

            <q-item-label header class="text-caption">Record Types</q-item-label>

            <q-item 
              clickable 
              :active="selectedDoc === 'hpdb-records'"
              @click="loadDoc('Input_File_Specification/record_types/hpdb_records.md', 'hpdb-records')"
              active-class="bg-blue-1"
            >
              <q-item-section>
                <q-item-label>HPDB Records</q-item-label>
              </q-item-section>
            </q-item>

            <q-item 
              clickable 
              :active="selectedDoc === 'system-records'"
              @click="loadDoc('Input_File_Specification/record_types/system_records.md', 'system-records')"
              active-class="bg-blue-1"
            >
              <q-item-section>
                <q-item-label>System Records</q-item-label>
              </q-item-section>
            </q-item>

            <q-item 
              clickable 
              :active="selectedDoc === 'favorites-records'"
              @click="loadDoc('Input_File_Specification/record_types/favorites_records.md', 'favorites-records')"
              active-class="bg-blue-1"
            >
              <q-item-section>
                <q-item-label>Favorites Records</q-item-label>
              </q-item-section>
            </q-item>

            <q-item 
              clickable 
              :active="selectedDoc === 'scan-records'"
              @click="loadDoc('Input_File_Specification/record_types/scan_records.md', 'scan-records')"
              active-class="bg-blue-1"
            >
              <q-item-section>
                <q-item-label>Scan Records</q-item-label>
              </q-item-section>
            </q-item>

            <q-item 
              clickable 
              :active="selectedDoc === 'profile-records'"
              @click="loadDoc('Input_File_Specification/record_types/scanner_profile_records.md', 'profile-records')"
              active-class="bg-blue-1"
            >
              <q-item-section>
                <q-item-label>Scanner/Profile Records</q-item-label>
              </q-item-section>
            </q-item>

            <q-item 
              clickable 
              :active="selectedDoc === 'discovery-records'"
              @click="loadDoc('Input_File_Specification/record_types/discovery_records.md', 'discovery-records')"
              active-class="bg-blue-1"
            >
              <q-item-section>
                <q-item-label>Discovery Records</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </q-expansion-item>

        <q-expansion-item
          expand-separator
          icon="table_chart"
          label="Reference Tables"
        >
          <q-list padding>
            <q-item 
              clickable 
              :active="selectedDoc === 'service-types'"
              @click="loadDoc('Input_File_Specification/reference_tables/service_types.md', 'service-types')"
              active-class="bg-blue-1"
            >
              <q-item-section>
                <q-item-label>Service Types</q-item-label>
              </q-item-section>
            </q-item>

            <q-item 
              clickable 
              :active="selectedDoc === 'freq-ctcss-dcs'"
              @click="loadDoc('Input_File_Specification/reference_tables/frequency_options_ctcss_dcs.md', 'freq-ctcss-dcs')"
              active-class="bg-blue-1"
            >
              <q-item-section>
                <q-item-label>CTCSS/DCS Options</q-item-label>
              </q-item-section>
            </q-item>

            <q-item 
              clickable 
              :active="selectedDoc === 'freq-p25'"
              @click="loadDoc('Input_File_Specification/reference_tables/frequency_options_p25.md', 'freq-p25')"
              active-class="bg-blue-1"
            >
              <q-item-section>
                <q-item-label>P25 NAC Options</q-item-label>
              </q-item-section>
            </q-item>

            <q-item 
              clickable 
              :active="selectedDoc === 'freq-dmr'"
              @click="loadDoc('Input_File_Specification/reference_tables/frequency_options_dmr.md', 'freq-dmr')"
              active-class="bg-blue-1"
            >
              <q-item-section>
                <q-item-label>DMR Color Code</q-item-label>
              </q-item-section>
            </q-item>

            <q-item 
              clickable 
              :active="selectedDoc === 'freq-nxdn'"
              @click="loadDoc('Input_File_Specification/reference_tables/frequency_options_nxdn.md', 'freq-nxdn')"
              active-class="bg-blue-1"
            >
              <q-item-section>
                <q-item-label>NXDN RAN/Area</q-item-label>
              </q-item-section>
            </q-item>

            <q-item 
              clickable 
              :active="selectedDoc === 'display-opts'"
              @click="loadDoc('Input_File_Specification/reference_tables/display_options.md', 'display-opts')"
              active-class="bg-blue-1"
            >
              <q-item-section>
                <q-item-label>Display Options</q-item-label>
              </q-item-section>
            </q-item>

            <q-item 
              clickable 
              :active="selectedDoc === 'display-colors'"
              @click="loadDoc('Input_File_Specification/reference_tables/display_colors.md', 'display-colors')"
              active-class="bg-blue-1"
            >
              <q-item-section>
                <q-item-label>Display Colors</q-item-label>
              </q-item-section>
            </q-item>

            <q-item 
              clickable 
              :active="selectedDoc === 'display-layouts'"
              @click="loadDoc('Input_File_Specification/reference_tables/display_layouts.md', 'display-layouts')"
              active-class="bg-blue-1"
            >
              <q-item-section>
                <q-item-label>Display Layouts</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </q-expansion-item>
      </q-list>
    </q-drawer>

    <q-page-container>
      <q-page class="q-pa-md">
        <div v-if="loading" class="flex flex-center q-pa-xl">
          <q-spinner color="primary" size="48px" />
        </div>

        <div v-else-if="error" class="text-center q-pa-xl">
          <q-icon name="error" size="48px" color="negative" />
          <div class="text-h6 q-mt-md">{{ error }}</div>
        </div>

        <div v-else-if="htmlContent" 
             class="markdown-content"
             v-html="htmlContent">
        </div>

        <div v-else class="text-center q-pa-xl text-grey-6">
          <q-icon name="description" size="64px" />
          <div class="text-h6 q-mt-md">Select a document from the menu</div>
        </div>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { marked } from 'marked'
import axios from 'axios'

const leftDrawerOpen = ref(true)
const selectedDoc = ref(null)
const htmlContent = ref('')
const loading = ref(false)
const error = ref(null)

// Configure marked for better rendering
marked.setOptions({
  gfm: true,
  breaks: false,
  headerIds: true,
  mangle: false
})

const loadDoc = async (path, docId) => {
  selectedDoc.value = docId
  loading.value = true
  error.value = null
  htmlContent.value = ''

  try {
    // Fetch markdown file from docs directory
    const response = await axios.get(`/docs/${path}`, {
      headers: { 'Accept': 'text/plain, text/markdown' }
    })
    
    // Convert markdown to HTML
    htmlContent.value = marked.parse(response.data)
  } catch (err) {
    console.error('Error loading documentation:', err)
    error.value = `Failed to load documentation: ${err.message}`
  } finally {
    loading.value = false
  }
}

// Load default document on mount
onMounted(() => {
  loadDoc('Input_File_Specification/README.md', 'spec-readme')
})
</script>

<style scoped>
.markdown-content {
  max-width: 1200px;
  margin: 0 auto;
  font-size: 15px;
  line-height: 1.6;
}

.markdown-content :deep(h1) {
  font-size: 2em;
  font-weight: 600;
  margin-top: 24px;
  margin-bottom: 16px;
  padding-bottom: 0.3em;
  border-bottom: 1px solid #e1e4e8;
}

.markdown-content :deep(h2) {
  font-size: 1.5em;
  font-weight: 600;
  margin-top: 24px;
  margin-bottom: 16px;
  padding-bottom: 0.3em;
  border-bottom: 1px solid #e1e4e8;
}

.markdown-content :deep(h3) {
  font-size: 1.25em;
  font-weight: 600;
  margin-top: 16px;
  margin-bottom: 8px;
}

.markdown-content :deep(h4) {
  font-size: 1em;
  font-weight: 600;
  margin-top: 16px;
  margin-bottom: 8px;
}

.markdown-content :deep(p) {
  margin-top: 0;
  margin-bottom: 16px;
}

.markdown-content :deep(code) {
  background-color: rgba(27, 31, 35, 0.05);
  border-radius: 3px;
  padding: 0.2em 0.4em;
  font-family: 'Courier New', Courier, monospace;
  font-size: 85%;
}

.markdown-content :deep(pre) {
  background-color: #f6f8fa;
  border-radius: 6px;
  padding: 16px;
  overflow: auto;
  margin-bottom: 16px;
}

.markdown-content :deep(pre code) {
  background-color: transparent;
  padding: 0;
  font-size: 100%;
}

.markdown-content :deep(table) {
  border-collapse: collapse;
  width: 100%;
  margin-bottom: 16px;
}

.markdown-content :deep(table th),
.markdown-content :deep(table td) {
  border: 1px solid #dfe2e5;
  padding: 8px 13px;
}

.markdown-content :deep(table th) {
  background-color: #f6f8fa;
  font-weight: 600;
}

.markdown-content :deep(table tr:nth-child(2n)) {
  background-color: #f6f8fa;
}

.markdown-content :deep(ul),
.markdown-content :deep(ol) {
  padding-left: 2em;
  margin-bottom: 16px;
}

.markdown-content :deep(li) {
  margin-top: 0.25em;
}

.markdown-content :deep(blockquote) {
  border-left: 4px solid #dfe2e5;
  color: #6a737d;
  padding: 0 1em;
  margin-bottom: 16px;
}

.markdown-content :deep(hr) {
  height: 0.25em;
  padding: 0;
  margin: 24px 0;
  background-color: #e1e4e8;
  border: 0;
}

.markdown-content :deep(a) {
  color: #0366d6;
  text-decoration: none;
}

.markdown-content :deep(a:hover) {
  text-decoration: underline;
}

.markdown-content :deep(img) {
  max-width: 100%;
  height: auto;
}
</style>
