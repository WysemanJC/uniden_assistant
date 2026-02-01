<template>
  <q-layout view="hHh Lpr fFf">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-btn flat dense round icon="menu" @click="leftDrawerOpen = !leftDrawerOpen" />
        <q-toolbar-title>Uniden Assistant</q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      :width="280"
      :breakpoint="500"
      bordered
    >
      <q-list>
        <q-item-label header>Navigation</q-item-label>
        
        <q-item 
          clickable 
          :active="activeSection === 'home'" 
          @click="activeSection = 'home'"
          active-class="bg-primary text-white"
        >
          <q-item-section avatar>
            <q-icon name="home" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Home</q-item-label>
          </q-item-section>
        </q-item>

        <q-expansion-item
          icon="folder"
          label="Data Management"
          default-opened
        >
          <q-item 
            clickable 
            :active="activeSection === 'database'" 
            @click="activeSection = 'database'"
            active-class="bg-primary text-white"
            class="q-pl-lg"
          >
            <q-item-section avatar>
              <q-icon name="storage" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Database</q-item-label>
            </q-item-section>
          </q-item>

          <q-item 
            clickable 
            :active="activeSection === 'favorites'" 
            @click="activeSection = 'favorites'"
            active-class="bg-primary text-white"
            class="q-pl-lg"
          >
            <q-item-section avatar>
              <q-icon name="star" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Favourites</q-item-label>
            </q-item-section>
          </q-item>

          <q-item 
            clickable 
            :active="activeSection === 'load-data'" 
            @click="activeSection = 'load-data'"
            active-class="bg-primary text-white"
            class="q-pl-lg"
          >
            <q-item-section avatar>
              <q-icon name="cloud_upload" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Load Data</q-item-label>
            </q-item-section>
          </q-item>
        </q-expansion-item>

        <q-expansion-item
          icon="description"
          label="File Specifications"
        >
          <q-item 
            clickable 
            :active="activeSection === 'spec-readme'"
            @click="loadSpec('Input_File_Specification/README.md', 'spec-readme')"
            active-class="bg-primary text-white"
            class="q-pl-lg"
          >
            <q-item-section>
              <q-item-label>Overview</q-item-label>
            </q-item-section>
          </q-item>

          <q-item 
            clickable 
            :active="activeSection === 'global-rules'"
            @click="loadSpec('Input_File_Specification/global_parsing_rules.md', 'global-rules')"
            active-class="bg-primary text-white"
            class="q-pl-lg"
          >
            <q-item-section>
              <q-item-label>Global Parsing Rules</q-item-label>
            </q-item-section>
          </q-item>

          <q-expansion-item
            icon="article"
            label="Record Types"
            header-class="q-pl-lg"
          >
            <q-item 
              clickable 
              :active="activeSection === 'hpdb-records'"
              @click="loadSpec('Input_File_Specification/record_types/hpdb_records.md', 'hpdb-records')"
              active-class="bg-primary text-white"
              class="q-pl-xl"
            >
              <q-item-section>
                <q-item-label>HPDB Records</q-item-label>
              </q-item-section>
            </q-item>

            <q-item 
              clickable 
              :active="activeSection === 'system-records'"
              @click="loadSpec('Input_File_Specification/record_types/system_records.md', 'system-records')"
              active-class="bg-primary text-white"
              class="q-pl-xl"
            >
              <q-item-section>
                <q-item-label>System Records</q-item-label>
              </q-item-section>
            </q-item>

            <q-item 
              clickable 
              :active="activeSection === 'favorites-records'"
              @click="loadSpec('Input_File_Specification/record_types/favorites_records.md', 'favorites-records')"
              active-class="bg-primary text-white"
              class="q-pl-xl"
            >
              <q-item-section>
                <q-item-label>Favorites Records</q-item-label>
              </q-item-section>
            </q-item>

            <q-item 
              clickable 
              :active="activeSection === 'scan-records'"
              @click="loadSpec('Input_File_Specification/record_types/scan_records.md', 'scan-records')"
              active-class="bg-primary text-white"
              class="q-pl-xl"
            >
              <q-item-section>
                <q-item-label>Scan Records</q-item-label>
              </q-item-section>
            </q-item>

            <q-item 
              clickable 
              :active="activeSection === 'profile-records'"
              @click="loadSpec('Input_File_Specification/record_types/scanner_profile_records.md', 'profile-records')"
              active-class="bg-primary text-white"
              class="q-pl-xl"
            >
              <q-item-section>
                <q-item-label>Scanner/Profile Records</q-item-label>
              </q-item-section>
            </q-item>

            <q-item 
              clickable 
              :active="activeSection === 'discovery-records'"
              @click="loadSpec('Input_File_Specification/record_types/discovery_records.md', 'discovery-records')"
              active-class="bg-primary text-white"
              class="q-pl-xl"
            >
              <q-item-section>
                <q-item-label>Discovery Records</q-item-label>
              </q-item-section>
            </q-item>
          </q-expansion-item>

          <q-expansion-item
            icon="table_chart"
            label="Reference Tables"
            header-class="q-pl-lg"
          >
            <q-item 
              clickable 
              :active="activeSection === 'service-types'"
              @click="loadSpec('Input_File_Specification/reference_tables/service_types.md', 'service-types')"
              active-class="bg-primary text-white"
              class="q-pl-xl"
            >
              <q-item-section>
                <q-item-label>Service Types</q-item-label>
              </q-item-section>
            </q-item>

            <q-item 
              clickable 
              :active="activeSection === 'freq-ctcss-dcs'"
              @click="loadSpec('Input_File_Specification/reference_tables/frequency_options_ctcss_dcs.md', 'freq-ctcss-dcs')"
              active-class="bg-primary text-white"
              class="q-pl-xl"
            >
              <q-item-section>
                <q-item-label>CTCSS/DCS Options</q-item-label>
              </q-item-section>
            </q-item>

            <q-item 
              clickable 
              :active="activeSection === 'freq-p25'"
              @click="loadSpec('Input_File_Specification/reference_tables/frequency_options_p25.md', 'freq-p25')"
              active-class="bg-primary text-white"
              class="q-pl-xl"
            >
              <q-item-section>
                <q-item-label>P25 NAC Options</q-item-label>
              </q-item-section>
            </q-item>

            <q-item 
              clickable 
              :active="activeSection === 'freq-dmr'"
              @click="loadSpec('Input_File_Specification/reference_tables/frequency_options_dmr.md', 'freq-dmr')"
              active-class="bg-primary text-white"
              class="q-pl-xl"
            >
              <q-item-section>
                <q-item-label>DMR Color Code</q-item-label>
              </q-item-section>
            </q-item>

            <q-item 
              clickable 
              :active="activeSection === 'freq-nxdn'"
              @click="loadSpec('Input_File_Specification/reference_tables/frequency_options_nxdn.md', 'freq-nxdn')"
              active-class="bg-primary text-white"
              class="q-pl-xl"
            >
              <q-item-section>
                <q-item-label>NXDN RAN/Area</q-item-label>
              </q-item-section>
            </q-item>

            <q-item 
              clickable 
              :active="activeSection === 'display-opts'"
              @click="loadSpec('Input_File_Specification/reference_tables/display_options.md', 'display-opts')"
              active-class="bg-primary text-white"
              class="q-pl-xl"
            >
              <q-item-section>
                <q-item-label>Display Options</q-item-label>
              </q-item-section>
            </q-item>

            <q-item 
              clickable 
              :active="activeSection === 'display-colors'"
              @click="loadSpec('Input_File_Specification/reference_tables/display_colors.md', 'display-colors')"
              active-class="bg-primary text-white"
              class="q-pl-xl"
            >
              <q-item-section>
                <q-item-label>Display Colors</q-item-label>
              </q-item-section>
            </q-item>

            <q-item 
              clickable 
              :active="activeSection === 'display-layouts'"
              @click="loadSpec('Input_File_Specification/reference_tables/display_layouts.md', 'display-layouts')"
              active-class="bg-primary text-white"
              class="q-pl-xl"
            >
              <q-item-section>
                <q-item-label>Display Layouts</q-item-label>
              </q-item-section>
            </q-item>
          </q-expansion-item>
        </q-expansion-item>
      </q-list>
    </q-drawer>

    <q-page-container>
      <q-page class="q-pa-md">
        
        <!-- Home Section -->
        <div v-if="activeSection === 'home'">
          <div class="text-h4 q-mb-md">HPDB and Favourites Statistics</div>
          <div class="text-body1 q-mb-lg">
            Live totals from the HPDB and Favourites databases.
          </div>

          <div class="row q-col-gutter-md">
            <div class="col-12 col-lg-6">
              <q-card flat bordered>
                <q-card-section>
                  <div class="text-h6 q-mb-sm">
                    <q-icon name="storage" color="primary" size="sm" class="q-mr-sm" />
                    HPDB Statistics
                  </div>
                  <div v-if="statsLoading" class="q-py-md">
                    <q-spinner color="primary" size="24px" />
                  </div>
                  <div v-else-if="hpdbStats" class="row q-col-gutter-sm">
                    <div class="col-6">
                      <div class="text-caption text-grey-7">Countries</div>
                      <div class="text-h6">{{ hpdbStats.countries }}</div>
                    </div>
                    <div class="col-6">
                      <div class="text-caption text-grey-7">States</div>
                      <div class="text-h6">{{ hpdbStats.states }}</div>
                    </div>
                    <div class="col-6">
                      <div class="text-caption text-grey-7">Counties</div>
                      <div class="text-h6">{{ hpdbStats.counties }}</div>
                    </div>
                    <div class="col-6">
                      <div class="text-caption text-grey-7">Agencies</div>
                      <div class="text-h6">{{ hpdbStats.agencies }}</div>
                    </div>
                    <div class="col-6">
                      <div class="text-caption text-grey-7">Systems</div>
                      <div class="text-h6">{{ hpdbStats.systems }}</div>
                    </div>
                    <div class="col-6">
                      <div class="text-caption text-grey-7">Departments</div>
                      <div class="text-h6">{{ hpdbStats.departments }}</div>
                    </div>
                    <div class="col-6">
                      <div class="text-caption text-grey-7">Channel Groups</div>
                      <div class="text-h6">{{ hpdbStats.channel_groups }}</div>
                    </div>
                    <div class="col-6">
                      <div class="text-caption text-grey-7">Channels</div>
                      <div class="text-h6">{{ hpdbStats.channels }}</div>
                    </div>
                    <div class="col-6">
                      <div class="text-caption text-grey-7">Frequencies</div>
                      <div class="text-h6">{{ hpdbStats.frequencies }}</div>
                    </div>
                    <div class="col-6">
                      <div class="text-caption text-grey-7">Conventional</div>
                      <div class="text-h6">{{ hpdbStats.system_types?.conventional || 0 }}</div>
                    </div>
                    <div class="col-6">
                      <div class="text-caption text-grey-7">Trunk</div>
                      <div class="text-h6">{{ hpdbStats.system_types?.trunk || 0 }}</div>
                    </div>
                  </div>
                  <div v-else class="text-body2 text-grey-7">No HPDB statistics available.</div>
                </q-card-section>
              </q-card>
            </div>

            <div class="col-12 col-lg-6">
              <q-card flat bordered>
                <q-card-section>
                  <div class="text-h6 q-mb-sm">
                    <q-icon name="star" color="primary" size="sm" class="q-mr-sm" />
                    Favourites Statistics
                  </div>
                  <div v-if="statsLoading" class="q-py-md">
                    <q-spinner color="primary" size="24px" />
                  </div>
                  <div v-else-if="favoritesStats" class="row q-col-gutter-sm">
                    <div class="col-6">
                      <div class="text-caption text-grey-7">Profiles</div>
                      <div class="text-h6">{{ favoritesStats.profiles }}</div>
                    </div>
                    <div class="col-6">
                      <div class="text-caption text-grey-7">Favourites Lists</div>
                      <div class="text-h6">{{ favoritesStats.favorites_lists }}</div>
                    </div>
                    <div class="col-6">
                      <div class="text-caption text-grey-7">Agencies</div>
                      <div class="text-h6">{{ favoritesStats.agencies }}</div>
                    </div>
                    <div class="col-6">
                      <div class="text-caption text-grey-7">Channel Groups</div>
                      <div class="text-h6">{{ favoritesStats.channel_groups }}</div>
                    </div>
                    <div class="col-6">
                      <div class="text-caption text-grey-7">Channels</div>
                      <div class="text-h6">{{ favoritesStats.channels }}</div>
                    </div>
                    <div class="col-6">
                      <div class="text-caption text-grey-7">Frequencies</div>
                      <div class="text-h6">{{ favoritesStats.frequencies }}</div>
                    </div>
                  </div>
                  <div v-else class="text-body2 text-grey-7">No favourites statistics available.</div>
                </q-card-section>
              </q-card>
            </div>
          </div>
        </div>

        <!-- Database Editor Section -->
        <div v-if="activeSection === 'database'">
          <div class="text-h5 q-mb-md">HomePatrol Database (HPDB)</div>
          <div class="text-body2 text-grey-7 q-mb-lg">
            Browse and search the Uniden Homepatrol database organized by Country &gt; State &gt; County
          </div>

          <div class="row q-col-gutter-md" style="height: calc(100vh - 280px);">
            <!-- Left Pane: Country/State/County Tree -->
            <div class="col-12 col-md-3">
              <q-card flat bordered style="height: 100%;">
                <q-card-section class="q-pa-sm">
                  <q-input
                    v-model="searchQuery"
                    label="Search..."
                    outlined
                    dense
                    class="q-mb-sm"
                  >
                    <template #prepend>
                      <q-icon name="search" />
                    </template>
                  </q-input>

                  <div class="text-caption text-weight-bold q-mb-sm">Hierarchy</div>
                  <div style="height: calc(100vh - 400px); overflow-y: auto;">
                    <q-tree
                      :nodes="hpdbTree"
                      node-key="id"
                      label-key="name"
                      children-key="children"
                      v-model:expanded="expandedNodes"
                      v-model:selected="selectedNode"
                      @lazy-load="onLazyLoad"
                      :filter="searchQuery"
                      :filter-method="filterMethod"
                      selected-color="primary"
                    >
                      <template #default-header="prop">
                        <div 
                          class="row items-center q-gutter-xs" 
                          style="flex: 1;"
                          :class="{ 'cursor-pointer': prop.node.type === 'county' }"
                          @click="prop.node.type === 'county' ? selectCounty(prop.node) : null"
                        >
                          <q-icon 
                            :name="getNodeIcon(prop.node)" 
                            :color="getNodeColor(prop.node)" 
                            size="sm"
                          />
                          <span class="text-body2">{{ prop.node.name }}</span>
                        </div>
                      </template>
                    </q-tree>
                  </div>
                </q-card-section>
              </q-card>
            </div>

            <!-- Middle Pane: County Systems/Departments -->
            <div class="col-12 col-md-3">
              <q-card flat bordered style="height: 100%;">
                <q-card-section class="q-pa-sm">
                  <div v-if="selectedCounty">
                    <div class="text-subtitle2 q-mb-sm">{{ selectedCounty.name }}</div>
                    <div class="text-caption text-grey-7 q-mb-md">Systems & Departments</div>
                  </div>
                  <div v-else class="text-caption text-grey-7 q-mb-md">
                    Select a county
                  </div>

                  <div style="height: calc(100vh - 400px); overflow-y: auto;">
                    <div v-if="selectedCounty && countyAgencies.length > 0">
                      <q-list bordered separator>
                        <q-item
                          v-for="agency in countyAgencies"
                          :key="agency.id"
                          clickable
                          :active="selectedAgency && selectedAgency.id === agency.id"
                          active-class="bg-blue-1"
                          @click="selectAgency(agency)"
                        >
                          <q-item-section avatar>
                            <q-icon name="radio" color="primary" />
                          </q-item-section>
                          <q-item-section>
                            <q-item-label>{{ agency.name }}</q-item-label>
                            <q-item-label caption>
                              {{ agency.system_type }}
                            </q-item-label>
                          </q-item-section>
                          <q-item-section side>
                            <q-badge 
                              v-if="agency.group_count" 
                              :label="agency.group_count" 
                              color="blue" 
                            />
                          </q-item-section>
                        </q-item>
                      </q-list>
                    </div>
                    <div v-else-if="selectedCounty && !loadingAgencies && countyAgencies.length === 0" class="text-center q-pa-lg text-grey-7">
                      <q-icon name="info" size="2em" />
                      <div class="q-mt-md text-caption">No systems in this county</div>
                    </div>
                    <div v-else-if="loadingAgencies" class="text-center q-pa-lg">
                      <q-spinner color="primary" size="2em" />
                    </div>
                  </div>
                </q-card-section>
              </q-card>
            </div>

            <!-- Right Pane: Frequency List -->
            <div class="col-12 col-md-6">
              <q-card flat bordered style="height: 100%;">
                <q-card-section class="q-pa-sm">
                  <div v-if="selectedAgency">
                    <div class="row items-center q-mb-md">
                      <div class="col">
                        <div class="text-h6">{{ selectedAgency.name }}</div>
                        <div class="text-caption text-grey-7">
                          {{ selectedAgency.system_type }} System
                        </div>
                      </div>
                      <div class="col-auto">
                        <q-btn 
                          flat 
                          color="primary" 
                          icon="open_in_new" 
                          size="sm"
                          label="Details"
                          @click="openAgencyDetail(selectedAgency)"
                        />
                      </div>
                    </div>

                    <q-separator class="q-mb-md" />

                    <div v-if="loadingFrequencies" class="text-center q-pa-xl">
                      <q-spinner color="primary" size="2em" />
                      <div class="q-mt-md text-grey-7 text-caption">Loading frequencies...</div>
                    </div>

                    <div v-else-if="agencyFrequencies.length > 0">
                      <div class="text-caption text-weight-bold q-mb-sm">Frequencies ({{ agencyFrequencies.length }})</div>
                      <q-table
                        :rows="agencyFrequencies"
                        :columns="frequencyColumns"
                        row-key="id"
                        flat
                        dense
                        :rows-per-page-options="[0]"
                        virtual-scroll
                        style="max-height: calc(100vh - 480px);"
                      >
                        <template #body-cell-enabled="props">
                          <q-td :props="props">
                            <q-icon 
                              :name="props.value ? 'check_circle' : 'cancel'" 
                              :color="props.value ? 'positive' : 'grey'"
                              size="xs"
                            />
                          </q-td>
                        </template>
                        <template #body-cell-frequency="props">
                          <q-td :props="props">
                            {{ (props.value / 1000000).toFixed(4) }} MHz
                          </q-td>
                        </template>
                      </q-table>
                    </div>

                    <div v-else class="text-center q-pa-xl text-grey-7">
                      <q-icon name="info" size="2em" />
                      <div class="q-mt-md text-caption">No frequencies found</div>
                    </div>
                  </div>

                  <div v-else class="text-center q-pa-xl text-grey-7">
                    <q-icon name="radio" size="3em" />
                    <div class="q-mt-md">Select a system/department from the middle pane</div>
                  </div>
                </q-card-section>
              </q-card>
            </div>
          </div>
        </div>

        <!-- Favourites Editor Section -->
        <div v-if="activeSection === 'favorites'">
          <div class="text-h5 q-mb-md">Favourites Editor</div>
          <div class="row q-mb-md q-gutter-sm">
            <q-btn
              color="primary"
              label="Export to SD Card Directory"
              icon="save"
              @click="exportToSd"
            />
            <q-btn
              color="secondary"
              label="New Profile"
              icon="add"
              @click="showCreateDialog = true"
            />
          </div>

          <q-table
            :rows="favorites"
            :columns="favoritesColumns"
            row-key="id"
            :loading="favoritesLoading"
            @row-click="openFavoriteDetail"
            class="cursor-pointer"
          />
        </div>

        <!-- Load Data Section -->
        <div v-if="activeSection === 'load-data'">
          <div class="text-h5 q-mb-md">Load Data</div>
          <div class="text-body2 text-grey-7 q-mb-lg">
            Upload HPDB database files or favourites files.
          </div>

          <div class="row q-col-gutter-md">
            <div class="col-12 col-md-6">
              <q-card flat bordered>
                <q-card-section>
                  <div class="row items-center">
                    <div class="col">
                      <div class="text-h6 q-mb-sm">
                        <q-icon name="storage" color="primary" size="sm" class="q-mr-sm" />
                        Load HPDB Database
                      </div>
                      <div class="text-body2">
                        Select a directory containing hpdb.cfg and s_*.hpd files.
                      </div>
                    </div>
                    <div class="col-auto q-gutter-sm">
                      <q-btn
                        outline
                        color="primary"
                        label="Re-parse From Last Loaded Data"
                        :loading="hpdbImportLoading"
                        @click="reloadHpdbFromRaw"
                      />
                      <q-btn
                        outline
                        color="negative"
                        label="Clear Existing Data"
                        @click="clearHpdbDataConfirm"
                      />
                    </div>
                  </div>
                  <q-file
                    ref="hpdbFilePicker"
                    v-model="hpdbFiles"
                    class="q-mt-md"
                    filled
                    multiple
                    use-chips
                    label="Select HPDB directory"
                    accept=".cfg,.hpd"
                    :directory="true"
                    :webkitdirectory="true"
                  />
                  <div v-if="hpdbImportProgress.status !== 'idle'" class="q-mt-md">
                    <div class="text-caption text-grey-7">
                      <span v-if="hpdbImportProgress.currentFile">
                        Processing: {{ hpdbImportProgress.currentFile }}
                      </span>
                      <span v-else>
                        Preparing HPDB import...
                      </span>
                    </div>
                    <q-linear-progress
                      :value="hpdbImportProgressPercent"
                      color="primary"
                      class="q-mt-xs"
                    />
                    <div class="text-caption text-grey-7 q-mt-xs">
                      {{ hpdbImportProgress.processedFiles }} / {{ hpdbImportProgress.totalFiles }} files
                    </div>
                    <div v-if="hpdbImportProgress.status === 'processing'" class="text-caption text-primary q-mt-md">
                      <q-icon name="info" size="xs" />
                      Safe to navigate away - processing continues in background
                    </div>
                  </div>
                </q-card-section>
                <q-card-actions>
                  <q-btn
                    outline
                    color="primary"
                    label="Choose Directory"
                    @click="openHpdbPicker"
                  />
                  <q-btn
                    outline
                    color="primary"
                    label="Load HPDB"
                    :loading="hpdbImportLoading"
                    :disable="!hasHpdbFiles"
                    @click="importHpdb"
                  />
                </q-card-actions>
              </q-card>
            </div>

            <div class="col-12 col-md-6">
              <q-card flat bordered>
                <q-card-section>
                  <div class="text-h6 q-mb-sm">
                    <q-icon name="star" color="primary" size="sm" class="q-mr-sm" />
                    Load Favourites
                  </div>
                  <div class="text-body2">
                    Select a directory containing f_list.cfg and favourites .hpd files.
                  </div>
                  <q-file
                    ref="favoritesFilePicker"
                    v-model="favoritesFiles"
                    class="q-mt-md"
                    filled
                    multiple
                    use-chips
                    label="Select Favourites directory"
                    accept=".cfg,.hpd"
                    :directory="true"
                    :webkitdirectory="true"
                  />
                </q-card-section>
                <q-card-actions>
                  <q-btn
                    outline
                    color="primary"
                    label="Choose Directory"
                    @click="openFavoritesPicker"
                  />
                  <q-btn
                    outline
                    color="primary"
                    label="Load Favourites"
                    :loading="favoritesImportLoading"
                    :disable="!hasFavoritesFiles"
                    @click="importFavorites"
                  />
                </q-card-actions>
              </q-card>
            </div>
          </div>
        </div>

        <!-- Specifications Section -->
        <div v-if="activeSection.startsWith('spec-') || activeSection.startsWith('global-') || 
                   activeSection.endsWith('-records') || activeSection.startsWith('service-') || 
                   activeSection.startsWith('freq-') || activeSection.startsWith('display-')">
          <div v-if="specLoading" class="flex flex-center q-pa-xl">
            <q-spinner color="primary" size="48px" />
          </div>

          <div v-else-if="specError" class="text-center q-pa-xl">
            <q-icon name="error" size="48px" color="negative" />
            <div class="text-h6 q-mt-md">{{ specError }}</div>
          </div>

          <div v-else-if="specContent" 
               class="markdown-content"
               v-html="specContent">
          </div>
        </div>

      </q-page>
    </q-page-container>

    <q-dialog v-model="showCreateDialog">
      <q-card style="min-width: 400px">
        <q-card-section class="row items-center q-pb-none">
          <div class="text-h6">Create New Profile</div>
          <q-space />
          <q-btn icon="close" flat round dense @click="showCreateDialog = false" />
        </q-card-section>

        <q-card-section>
          <q-input
            v-model="newProfile.name"
            label="Profile Name"
            class="q-mb-md"
          />
          <q-input
            v-model="newProfile.model"
            label="Scanner Model"
            class="q-mb-md"
          />
          <q-input
            v-model="newProfile.firmware_version"
            label="Firmware Version"
            class="q-mb-md"
          />
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancel" @click="showCreateDialog = false" />
          <q-btn
            flat
            label="Create"
            color="primary"
            @click="createNewProfile"
            :loading="scanner.loading"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- SD card import dialog removed; use Load Data page uploads -->
  </q-layout>
</template>
<script setup>
import { ref, onMounted, computed, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useScannerStore } from '../stores/scanner'
import api, { sdAPI } from '../api'
import { useQuasar, QSeparator } from 'quasar'
import { marked } from 'marked'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const scanner = useScannerStore()
const $q = useQuasar()

// Configure marked for better rendering
marked.setOptions({
  gfm: true,
  breaks: false,
  headerIds: true,
  mangle: false
})

// Navigation
const leftDrawerOpen = ref(true)
const activeSection = ref('home')

// Specifications
const specContent = ref('')
const specLoading = ref(false)
const specError = ref(null)

// HPDB Tree
const hpdbTree = ref([])
const expandedNodes = ref([])
const selectedNode = ref(null)
const searchQuery = ref('')
const hpdbImportLoading = ref(false)
const favoritesImportLoading = ref(false)
const statsLoading = ref(false)
const hpdbStats = ref(null)
const favoritesStats = ref(null)
const hpdbImportProgress = ref({
  status: 'idle',
  stage: '',
  currentFile: '',
  processedFiles: 0,
  totalFiles: 0
})
const hpdbImportProgressPercent = computed(() => {
  const total = hpdbImportProgress.value.totalFiles || 0
  if (!total) {
    return 0
  }
  return Math.min(1, hpdbImportProgress.value.processedFiles / total)
})

// Agency Details and Frequencies
const selectedCounty = ref(null)
const selectedAgency = ref(null)
const countyAgencies = ref([])
const agencyFrequencies = ref([])
const loadingAgencies = ref(false)
const loadingFrequencies = ref(false)

const frequencyColumns = [
  { name: 'group_name', label: 'Channel Group', field: 'group_name', align: 'left', sortable: true },
  { name: 'name', label: 'Name', field: 'name', align: 'left', sortable: true },
  { name: 'frequency', label: 'Frequency', field: 'frequency', align: 'left', sortable: true },
  { name: 'modulation', label: 'Modulation', field: 'modulation', align: 'left', sortable: true },
  { name: 'tone', label: 'Tone/NAC', field: 'tone', align: 'left', sortable: true },
  { name: 'enabled', label: 'Enabled', field: 'enabled', align: 'center' }
]

// Favourites
const favorites = ref([])
const favoritesLoading = ref(false)
const favoritesColumns = [
  { name: 'name', label: 'Name', field: 'name', align: 'left' },
  { name: 'filename', label: 'File', field: 'filename', align: 'left' },
  { name: 'enabled', label: 'Enabled', field: 'enabled', align: 'center' },
  { name: 'disabled_on_power', label: 'Disable on Power Up', field: 'disabled_on_power', align: 'center' },
  { name: 'quick_key', label: 'Quick Key', field: 'quick_key', align: 'center' },
  { name: 'list_number', label: 'List #', field: 'list_number', align: 'center' }
]

const showCreateDialog = ref(false)
const hpdbFiles = ref([])
const favoritesFiles = ref([])
const hpdbFilePicker = ref(null)
const favoritesFilePicker = ref(null)
const hasHpdbFiles = computed(() => {
  const files = Array.isArray(hpdbFiles.value)
    ? hpdbFiles.value
    : Array.from(hpdbFiles.value || [])
  return files.length > 0
})
const hasFavoritesFiles = computed(() => {
  const files = Array.isArray(favoritesFiles.value)
    ? favoritesFiles.value
    : Array.from(favoritesFiles.value || [])
  return files.length > 0
})
const newProfile = ref({
  name: '',
  model: '',
  firmware_version: ''
})

onMounted(() => {
  // Check for section query parameter
  const section = route.query.section
  if (section && ['home', 'database', 'favorites'].includes(section)) {
    activeSection.value = section
  }
  
  scanner.fetchProfiles()
  loadHPDBTree()
  loadFavoritesList()
  loadStats()
})

onBeforeUnmount(() => {
  stopHpdbImportPolling()
})

const loadStats = async () => {
  statsLoading.value = true
  try {
    const [hpdbResp, favResp] = await Promise.all([
      api.get('/uniden_manager/hpdb/stats/'),
      api.get('/uniden_manager/usersettings/stats/')
    ])
    hpdbStats.value = hpdbResp.data
    favoritesStats.value = favResp.data
  } catch (error) {
    $q.notify({ type: 'negative', message: 'Failed to load statistics' })
  } finally {
    statsLoading.value = false
  }
}

// HPDB Tree Methods
const loadHPDBTree = async () => {
  try {
    const { data } = await api.get('/uniden_manager/hpdb/tree/tree/')
    hpdbTree.value = data
  } catch (error) {
    console.error('Error loading HPDB tree:', error)
    $q.notify({ type: 'negative', message: 'Failed to load database tree' })
  }
}

const expandAgencyGroups = async (agencyId) => {
  try {
    // Extract numeric ID from node ID (e.g., "agency-268" -> "268")
    const numericId = agencyId.toString().replace('agency-', '')
    const { data } = await api.get(`/uniden_manager/hpdb/channel-groups/?agency=${numericId}`)
    // Handle paginated response
    const groups = data.results || []
    return groups.map(group => ({
      id: `group-${group.id}`,
      type: 'group',
      name: group.name,
      location_type: group.location_type,
      latitude: group.latitude,
      longitude: group.longitude,
      range_miles: group.range_miles,
      frequency_count: group.frequency_count
    }))
  } catch (error) {
    console.error('Error loading channel groups:', error)
    return []
  }
}

const loadFavoritesList = async () => {
  favoritesLoading.value = true
  try {
    const { data } = await api.get('/usersettings/favorites-lists/')
    // Handle paginated response
    favorites.value = Array.isArray(data) ? data : (data.results || [])
  } catch (error) {
    console.error('Error loading favorites list:', error)
    $q.notify({ type: 'negative', message: 'Failed to load favourites list' })
  } finally {
    favoritesLoading.value = false
  }
}

const openFavoriteDetail = (evt, row) => {
  router.push(`/favorite/${row.id}`)
}

const selectCounty = async (node) => {
  selectedCounty.value = node
  selectedAgency.value = null
  agencyFrequencies.value = []
  loadingAgencies.value = true
  countyAgencies.value = []
  
  try {
    // Extract numeric ID from node ID (e.g., "county-268" -> "268")
    const numericId = node.id.toString().replace('county-', '')
    
    // Load agencies for this county
    const { data: agenciesResponse } = await api.get(`/uniden_manager/hpdb/tree/agencies/?county=county-${numericId}`)
    countyAgencies.value = agenciesResponse
  } catch (error) {
    console.error('Error loading county agencies:', error)
    $q.notify({ type: 'negative', message: 'Failed to load systems' })
  } finally {
    loadingAgencies.value = false
  }
}

const selectAgency = async (node) => {
  selectedAgency.value = node
  loadingFrequencies.value = true
  agencyFrequencies.value = []
  
  try {
    // Extract numeric ID from node ID (e.g., "agency-268" -> "268")
    const numericId = node.id.toString().replace('agency-', '')
    
    // Load channel groups for this agency
    const { data: groupsResponse } = await api.get(`/uniden_manager/hpdb/channel-groups/?agency=${numericId}`)
    const groups = Array.isArray(groupsResponse) ? groupsResponse : (groupsResponse.results || [])
    
    // Load frequencies for each group
    const allFrequencies = []
    for (const group of groups) {
      try {
        const { data: freqData } = await api.get(`/uniden_manager/hpdb/frequencies/?channel_group=${group.id}`)
        const frequencies = Array.isArray(freqData) ? freqData : (freqData.results || [])
        // Add group name to each frequency for context
        frequencies.forEach(freq => {
          allFrequencies.push({
            ...freq,
            group_name: group.name
          })
        })
      } catch (error) {
        console.error(`Error loading frequencies for group ${group.id}:`, error)
      }
    }
    
    agencyFrequencies.value = allFrequencies
  } catch (error) {
    console.error('Error loading agency frequencies:', error)
    $q.notify({ type: 'negative', message: 'Failed to load frequencies' })
  } finally {
    loadingFrequencies.value = false
  }
}

const getNodeIcon = (node) => {
  switch (node.type) {
    case 'country': return 'public'
    case 'state': return 'map'
    case 'county': return 'location_city'
    case 'agency': return 'radio'
    case 'group': return 'waves'
    default: return 'folder'
  }
}

const getNodeColor = (node) => {
  switch (node.type) {
    case 'country': return 'blue'
    case 'state': return 'green'
    case 'county': return 'orange'
    case 'agency': return node.enabled ? 'primary' : 'grey'
    case 'group': return 'purple'
    default: return 'grey'
  }
}

const onLazyLoad = ({ node, key, done, fail }) => {
  // Only lazy load counties for states; counties are leaf nodes
  if (node.type === 'state') {
    // Load counties for the state
    const stateId = node.id
    api.get(`/uniden_manager/hpdb/tree/counties/?state=${stateId}`)
      .then(({ data }) => {
        done(data)
      })
      .catch(error => {
        console.error('Error loading counties:', error)
        fail()
        $q.notify({ type: 'negative', message: 'Failed to load counties' })
      })
  } else {
    // No lazy loading for other node types in the tree
    done([])
  }
}

const filterMethod = (node, filter) => {
  const filt = filter.toLowerCase()
  return node.name.toLowerCase().includes(filt)
}

const openAgencyDetail = (node) => {
  // Extract numeric ID from node.id (format is "agency-123")
  const agencyId = node.id.toString().replace('agency-', '')
  router.push(`/database/${agencyId}`)
}

// Import/Export Methods

const validateHpdbFiles = (files) => {
  const names = files.map(f => f.name.toLowerCase())
  const hasCfg = names.includes('hpdb.cfg')
  const hasSystem = names.some(n => n.startsWith('s_') && n.endsWith('.hpd'))
  return { hasCfg, hasSystem }
}

const validateFavoritesFiles = (files) => {
  const names = files.map(f => f.name.toLowerCase())
  const hasCfg = names.includes('f_list.cfg')
  const hasHpd = names.some(n => n.endsWith('.hpd'))
  return { hasCfg, hasHpd }
}

const triggerFilePicker = (pickerRef) => {
  const el = pickerRef?.value?.$el
  const input = el?.querySelector('input[type="file"]')
  input?.click()
}

const openHpdbPicker = () => {
  triggerFilePicker(hpdbFilePicker)
}

const openFavoritesPicker = () => {
  triggerFilePicker(favoritesFilePicker)
}

let hpdbImportTimer = null

const resetHpdbImportProgress = () => {
  hpdbImportProgress.value = {
    status: 'idle',
    stage: '',
    currentFile: '',
    processedFiles: 0,
    totalFiles: 0
  }
}

const stopHpdbImportPolling = () => {
  if (hpdbImportTimer) {
    clearInterval(hpdbImportTimer)
    hpdbImportTimer = null
  }
}

const startHpdbImportPolling = (jobId) => {
  stopHpdbImportPolling()

  const poll = async () => {
    try {
      const { data } = await api.get('/hpdb/import-progress/', {
        params: { job_id: jobId }
      })

      hpdbImportProgress.value = {
        status: data.status || 'processing',
        stage: data.stage || '',
        currentFile: data.current_file || '',
        processedFiles: data.processed_files || 0,
        totalFiles: data.total_files || 0
      }

      if (data.status === 'completed') {
        stopHpdbImportPolling()
        hpdbImportLoading.value = false
        if (data.result?.systems !== undefined) {
          $q.notify({ type: 'positive', message: `HPDB import completed (${data.result.systems} files)` })
        } else {
          $q.notify({ type: 'positive', message: 'HPDB import completed' })
        }
        await loadHPDBTree()
        setTimeout(resetHpdbImportProgress, 2000)
      } else if (data.status === 'failed') {
        stopHpdbImportPolling()
        hpdbImportLoading.value = false
        $q.notify({ type: 'negative', message: 'HPDB import failed: ' + (data.error_message || 'Unknown error') })
      }
    } catch (error) {
      stopHpdbImportPolling()
      hpdbImportLoading.value = false
      $q.notify({ type: 'negative', message: 'HPDB import failed: ' + (error.response?.data?.error || error.message) })
    }
  }

  poll()
  hpdbImportTimer = setInterval(poll, 1000)
}

const importHpdb = async () => {
  const files = Array.isArray(hpdbFiles.value)
    ? hpdbFiles.value
    : Array.from(hpdbFiles.value || [])
  if (files.length === 0) {
    openHpdbPicker()
    return
  }
  const { hasCfg, hasSystem } = validateHpdbFiles(files)
  if (!hasCfg || !hasSystem) {
    $q.notify({ type: 'negative', message: 'HPDB upload requires hpdb.cfg and at least one s_*.hpd file.' })
    return
  }

  hpdbImportLoading.value = true
  hpdbImportProgress.value = {
    status: 'uploading',
    stage: 'upload',
    currentFile: '',
    processedFiles: 0,
    totalFiles: files.filter(file => file.name.toLowerCase().startsWith('s_') && file.name.toLowerCase().endsWith('.hpd')).length
  }
  try {
    const formData = new FormData()
    files.forEach(file => formData.append('files', file))
    const { data } = await api.post('/hpdb/import-files/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    if (!data.job_id) {
      throw new Error('Missing job id from import response')
    }
    startHpdbImportPolling(data.job_id)
  } catch (error) {
    stopHpdbImportPolling()
    $q.notify({ type: 'negative', message: 'HPDB import failed: ' + (error.response?.data?.error || error.message) })
    hpdbImportLoading.value = false
    resetHpdbImportProgress()
  } finally {
    // Loading state handled by progress polling
  }
}

const reloadHpdbFromRaw = () => {
  $q.dialog({
    title: 'Re-parse HPDB From Last Loaded Data',
    message: 'This will rebuild all HPDB data (countries, states, counties, agencies, channel groups, frequencies) from the most recently loaded raw files. The raw data itself will not be deleted. Continue?',
    ok: {
      label: 'Re-parse',
      color: 'primary'
    },
    cancel: true,
    persistent: true
  }).onOk(async () => {
    hpdbImportLoading.value = true
    hpdbImportProgress.value = {
      status: 'processing',
      stage: 'systems',
      currentFile: '',
      processedFiles: 0,
      totalFiles: 0
    }
    try {
      const { data } = await api.post('/hpdb/reload-from-raw/')
      if (!data.job_id) {
        throw new Error('Missing job id from reload response')
      }
      startHpdbImportPolling(data.job_id)
    } catch (error) {
      stopHpdbImportPolling()
      $q.notify({ type: 'negative', message: 'HPDB re-parse failed: ' + (error.response?.data?.error || error.message) })
      hpdbImportLoading.value = false
      resetHpdbImportProgress()
    }
  })
}

const clearHpdbDataConfirm = () => {
  $q.dialog({
    title: 'Clear HPDB Data',
    message: 'Delete all HPDB database records? This cannot be undone.',
    ok: {
      label: 'Delete',
      color: 'negative'
    },
    cancel: true,
    persistent: true
  }).onOk(() => {
    clearHpdbData()
  })
}

const clearHpdbData = async () => {
  try {
    await api.post('/hpdb/clear-data/')
    $q.notify({ type: 'positive', message: 'HPDB data cleared successfully' })
    await loadHPDBTree()
  } catch (error) {
    $q.notify({ type: 'negative', message: 'Failed to clear HPDB data: ' + (error.response?.data?.error || error.message) })
  }
}

const importFavorites = async () => {
  const files = Array.isArray(favoritesFiles.value)
    ? favoritesFiles.value
    : Array.from(favoritesFiles.value || [])
  if (files.length === 0) {
    openFavoritesPicker()
    return
  }
  const { hasCfg, hasHpd } = validateFavoritesFiles(files)
  if (!hasCfg || !hasHpd) {
    $q.notify({ type: 'negative', message: 'Favourites upload requires f_list.cfg and at least one .hpd file.' })
    return
  }

  favoritesImportLoading.value = true
  try {
    const formData = new FormData()
    files.forEach(file => formData.append('files', file))
    const { data } = await api.post('/usersettings/import-files/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    if (data.errors?.length) {
      $q.notify({ type: 'warning', message: `Imported with ${data.errors.length} error(s)` })
    } else {
      $q.notify({ type: 'positive', message: `Imported ${data.imported} profile(s)` })
    }
    await scanner.fetchProfiles()
    await loadFavoritesList()
  } catch (error) {
    $q.notify({ type: 'negative', message: 'Favourites import failed: ' + (error.response?.data?.error || error.message) })
  } finally {
    favoritesImportLoading.value = false
  }
}

const exportToSd = async () => {
  try {
    const { data } = await sdAPI.exportToSd()
    if (data.errors?.length) {
      $q.notify({ type: 'warning', message: `Exported with ${data.errors.length} error(s)` })
    } else {
      $q.notify({ type: 'positive', message: `Exported ${data.exported} profile(s)` })
    }
  } catch (error) {
    $q.notify({ type: 'negative', message: 'Export failed: ' + error.message })
  }
}

const createNewProfile = async () => {
  try {
    await scanner.createProfile(newProfile.value)
    showCreateDialog.value = false
    newProfile.value = { name: '', model: '', firmware_version: '' }
  } catch (error) {
    console.error('Error creating profile:', error)
  }
}

const openProfile = (row) => {
  router.push(`/profile/${row.id}`)
}

const deleteProfile = async (id) => {
  if (confirm('Are you sure you want to delete this profile?')) {
    try {
      await scanner.deleteProfile(id)
    } catch (error) {
      console.error('Error deleting profile:', error)
    }
  }
}

// Specifications Methods
const loadSpec = async (path, sectionId) => {
  activeSection.value = sectionId
  specLoading.value = true
  specError.value = null
  specContent.value = ''

  try {
    // Fetch markdown file from docs directory
    const response = await axios.get(`/docs/${path}`, {
      headers: { 'Accept': 'text/plain, text/markdown' }
    })
    
    // Convert markdown to HTML
    specContent.value = marked.parse(response.data)
  } catch (err) {
    console.error('Error loading documentation:', err)
    specError.value = `Failed to load documentation: ${err.message}`
  } finally {
    specLoading.value = false
  }
}
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
