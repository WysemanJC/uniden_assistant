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
                      label-key="name_tag"
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
                          class="row items-center q-gutter-xs cursor-pointer" 
                          style="flex: 1;"
                          @click.stop="selectNode(prop.node)"
                        >
                          <q-icon 
                            :name="getNodeIcon(prop.node)" 
                            :color="getNodeColor(prop.node)" 
                            size="sm"
                          />
                          <span class="text-body2">{{ prop.node.name_tag }}</span>
                          <q-badge 
                            v-if="prop.node.type === 'agency' && prop.node.group_count"
                            :label="prop.node.group_count"
                            color="blue"
                            class="q-ml-xs"
                          />
                        </div>
                      </template>
                    </q-tree>
                  </div>
                </q-card-section>
              </q-card>
            </div>

            <!-- Right Pane: Frequency List or Channel Groups -->
            <div class="col-12 col-md-9">
              <q-card flat bordered style="height: 100%;">
                <q-card-section class="q-pa-sm">
                  <!-- Show Agencies when County is selected -->
                  <div v-if="selectedCounty && !selectedAgency">
                    <div class="row items-center q-mb-md">
                      <div class="col">
                        <div class="text-h6">{{ selectedCounty.name_tag }}</div>
                        <div class="text-caption text-grey-7">Agencies</div>
                      </div>
                    </div>

                    <div v-if="countyAgencies.length > 0" style="height: calc(100vh - 340px); overflow-y: auto;">
                      <q-table
                        :rows="countyAgencies"
                        :columns="agencyColumns"
                        row-key="id"
                        flat
                        dense
                        :rows-per-page-options="[0]"
                        virtual-scroll
                        @row-click="onAgencyRowClick"
                        style="max-height: calc(100vh - 340px); cursor: pointer;"
                      >
                        <template #body-cell-avoid="props">
                          <q-td :props="props">
                            {{ props.value }}
                          </q-td>
                        </template>
                      </q-table>
                    </div>

                    <div v-else-if="loadingFrequencies" class="text-center q-pa-xl">
                      <q-spinner color="primary" size="2em" />
                      <div class="q-mt-md text-caption">Loading agencies...</div>
                    </div>

                    <div v-else class="text-center q-pa-xl text-grey-7">
                      <q-icon name="info" size="2em" />
                      <div class="q-mt-md text-caption">No agencies found</div>
                    </div>
                  </div>

                  <!-- Show Channel Groups when Agency is selected -->
                  <div v-else-if="selectedAgency && !selectedChannelGroup">
                    <div class="row items-center q-mb-md">
                      <div class="col">
                        <div class="text-h6">{{ selectedAgency.name_tag }}</div>
                        <div class="text-caption text-grey-7">Channel Groups</div>
                      </div>
                    </div>

                    <div v-if="agencyChannelGroups.length > 0" style="height: calc(100vh - 340px); overflow-y: auto;">
                      <q-table
                        :rows="agencyChannelGroups"
                        :columns="channelGroupColumns"
                        row-key="id"
                        flat
                        dense
                        :rows-per-page-options="[0]"
                        virtual-scroll
                        @row-click="onChannelGroupRowClick"
                        style="max-height: calc(100vh - 340px); cursor: pointer;"
                      >
                        <template #body-cell-avoid="props">
                          <q-td :props="props">
                            <q-icon 
                              :name="props.row.enabled ? 'check_circle' : 'cancel'" 
                              :color="props.row.enabled ? 'grey' : 'negative'"
                              size="xs"
                            />
                          </q-td>
                        </template>
                        <template #body-cell-system_type="props">
                          <q-td :props="props" class="cursor-pointer">
                            <div class="row items-center q-gutter-xs">
                              <span>{{ props.value }}</span>
                              <q-btn
                                v-if="(props.row.latitude && props.row.longitude) || (Array.isArray(props.row.rectangles) && props.row.rectangles.length > 0)"
                                flat
                                dense
                                size="sm"
                                icon="map"
                                color="primary"
                                @click.stop="openChannelGroupMap(props.row)"
                              />
                            </div>
                          </q-td>
                        </template>
                      </q-table>
                    </div>

                    <div v-else-if="loadingFrequencies" class="text-center q-pa-xl">
                      <q-spinner color="primary" size="2em" />
                      <div class="q-mt-md text-caption">Loading channel groups...</div>
                    </div>

                    <div v-else class="text-center q-pa-xl text-grey-7">
                      <q-icon name="info" size="2em" />
                      <div class="q-mt-md text-caption">No channel groups found</div>
                    </div>
                  </div>

                  <!-- Show Frequencies when Channel Group is selected -->
                  <div v-else-if="selectedChannelGroup">
                    <div class="row items-center q-mb-md">
                      <div class="col">
                        <div class="text-h6">{{ selectedChannelGroup.name_tag }}</div>
                        <div class="text-caption text-grey-7">
                          {{ selectedAgency?.name_tag || 'Agency' }}
                        </div>
                      </div>
                      <div class="col-auto">
                        <q-btn 
                          flat 
                          color="primary" 
                          icon="open_in_new" 
                          size="sm"
                          label="Details"
                          @click="openChannelGroupDetail(selectedChannelGroup)"
                        />
                      </div>
                    </div>

                    <q-separator class="q-mb-md" />

                    <div v-if="loadingFrequencies" class="text-center q-pa-xl">
                      <q-spinner color="primary" size="2em" />
                      <div class="q-mt-md text-grey-7 text-caption">Loading frequencies...</div>
                    </div>

                    <div v-else-if="channelGroupFrequencies.length > 0">
                      <div class="text-caption text-weight-bold q-mb-sm">Frequencies ({{ channelGroupFrequencies.length }})</div>
                      <q-table
                        :rows="channelGroupFrequencies"
                        :columns="frequencyColumns"
                        row-key="id"
                        flat
                        dense
                        :rows-per-page-options="[0]"
                        virtual-scroll
                        style="max-height: calc(100vh - 480px);"
                      >
                        <template #body-cell-avoid="props">
                          <q-td :props="props">
                            <q-icon 
                              :name="props.row.enabled ? 'check_circle' : 'cancel'" 
                              :color="props.row.enabled ? 'grey' : 'negative'"
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
                    <q-icon name="waves" size="3em" />
                    <div class="q-mt-md">Select a system/department to view frequencies</div>
                  </div>
                </q-card-section>
              </q-card>
            </div>
          </div>
        </div>

        <!-- Favourites Editor Section -->
        <div v-if="activeSection === 'favorites'">
          <div class="text-h5 q-mb-md">Scanner Favourites</div>
          <div class="row q-mb-md q-gutter-sm">
            <q-btn
              color="secondary"
              label="New Favorites List"
              icon="add"
              @click="createNewFavoritesList"
            />
            <q-btn
              color="negative"
              label="Delete Favorites List"
              icon="delete"
              @click="deleteFavoritesList"
            />
          </div>

          <!-- Tree + Table Layout for Favorites -->
          <div class="row q-col-gutter-md">
            <!-- Left Pane: Favorites Lists Tree -->
            <div class="col-12 col-md-3">
              <q-card flat bordered style="height: 100%; min-height: 600px;">
                <q-card-section class="q-pa-sm">
                  <div class="text-subtitle2 q-mb-sm">Favourites Lists</div>
                  <q-tree
                    :nodes="favoritesTreeNodes"
                    node-key="id"
                    v-model:selected="selectedFavoritesNodeId"
                  >
                    <template v-slot:default-header="prop">
                      <div 
                        class="row items-center q-gutter-xs cursor-pointer" 
                        style="flex: 1;"
                        @click.stop="selectFavoritesNode(prop.node)"
                      >
                        <q-icon 
                          :name="getFavoritesNodeIcon(prop.node)" 
                          :color="getFavoritesNodeColor(prop.node)" 
                          size="sm"
                        />
                        <span class="text-body2">{{ prop.node.label }}</span>
                        <q-badge 
                          v-if="prop.node.type === 'department' && prop.node.channel_count"
                          :label="prop.node.channel_count"
                          color="blue"
                          class="q-ml-xs"
                        />
                      </div>
                    </template>
                  </q-tree>
                </q-card-section>
              </q-card>
            </div>

            <!-- Right Pane: Channels Table -->
            <div class="col-12 col-md-9">
              <q-card flat bordered style="height: 100%; min-height: 600px;">
                <q-card-section class="q-pa-sm">
                  <!-- Department/Channel Details View -->
                  <div v-if="selectedFavoritesNode && selectedFavoritesNode.type === 'department'">
                    <div class="row items-center q-mb-md">
                      <div class="col">
                        <div class="text-h6">{{ selectedFavoritesNode.label }}</div>
                        <div class="text-caption text-grey-7">{{ selectedFavoritesList?.user_name || 'Favorites List' }}</div>
                      </div>
                      <q-btn
                        flat
                        round
                        dense
                        icon="edit"
                        color="primary"
                        size="sm"
                        @click="editDepartment(selectedFavoritesNode.groupData)"
                        class="q-mr-sm"
                      >
                        <q-tooltip>Edit Department Name</q-tooltip>
                      </q-btn>
                      <q-btn
                        color="secondary"
                        label="Add Channel"
                        icon="add"
                        size="sm"
                        @click="showAddChannelDialog = true"
                      />
                    </div>

                    <div v-if="favoritesChannels.length > 0" style="height: calc(100vh - 380px); overflow-y: auto;">
                      <q-table
                        :rows="favoritesChannels"
                        :columns="favoritesChannelColumns"
                        row-key="id"
                        flat
                        dense
                        :rows-per-page-options="[0]"
                        virtual-scroll
                        style="max-height: calc(100vh - 380px);"
                      >
                        <template #body-cell-frequency="props">
                          <q-td :props="props">
                            <span v-if="selectedFavoritesNode.system_type === 'Conventional'">
                              {{ (props.value / 1000000).toFixed(4) }} MHz
                            </span>
                            <span v-else>
                              TGID: {{ props.value }}
                            </span>
                          </q-td>
                        </template>
                        <template #body-cell-enabled="props">
                          <q-td :props="props">
                            <q-icon 
                              :name="props.value ? 'check_circle' : 'cancel'" 
                              :color="props.value ? 'positive' : 'negative'"
                              size="xs"
                            />
                          </q-td>
                        </template>
                        <template #body-cell-actions="props">
                          <q-td :props="props">
                            <q-btn
                              flat
                              round
                              dense
                              icon="edit"
                              color="primary"
                              size="sm"
                              @click="editChannel(props.row)"
                            >
                              <q-tooltip>Edit Channel</q-tooltip>
                            </q-btn>
                          </q-td>
                        </template>
                      </q-table>
                    </div>

                    <div v-else class="text-center q-pa-xl text-grey-7">
                      <q-icon name="info" size="2em" />
                      <div class="q-mt-md text-caption">No channels found</div>
                    </div>
                  </div>

                  <!-- Departments List View (when Favorites List selected) -->
                  <div v-else-if="selectedFavoritesNode && selectedFavoritesNode.type === 'favorites_list'">
                    <div class="row items-center q-mb-md">
                      <div class="col">
                        <div class="text-h6">{{ selectedFavoritesNode.label }}</div>
                        <div class="text-caption text-grey-7">Departments</div>
                      </div>
                      <q-btn
                        flat
                        round
                        dense
                        icon="edit"
                        color="primary"
                        size="sm"
                        @click="editFavoritesList(selectedFavoritesNode.favData)"
                        class="q-mr-sm"
                      >
                        <q-tooltip>Edit Favorites List Name</q-tooltip>
                      </q-btn>
                      <q-btn
                        color="secondary"
                        label="Add Department"
                        icon="add"
                        size="sm"
                        @click="showAddDepartmentDialog = true"
                      />
                    </div>

                    <div v-if="selectedFavoritesNode.favData && selectedFavoritesNode.favData.groups && selectedFavoritesNode.favData.groups.length > 0" style="height: calc(100vh - 380px); overflow-y: auto;">
                      <q-table
                        :rows="selectedFavoritesNode.favData.groups"
                        :columns="favoritesListDepartmentColumns"
                        row-key="id"
                        flat
                        dense
                        :rows-per-page-options="[0]"
                        virtual-scroll
                        style="max-height: calc(100vh - 380px);"
                      >
                        <template #body-cell-actions="props">
                          <q-td :props="props">
                            <q-btn
                              flat
                              round
                              dense
                              icon="edit"
                              color="primary"
                              size="sm"
                              @click="editDepartment(props.row)"
                            >
                              <q-tooltip>Edit Department</q-tooltip>
                            </q-btn>
                          </q-td>
                        </template>
                      </q-table>
                    </div>

                    <div v-else class="text-center q-pa-xl text-grey-7">
                      <q-icon name="info" size="2em" />
                      <div class="q-mt-md text-caption">No departments found</div>
                    </div>
                  </div>

                  <!-- Default Message -->
                  <div v-else class="text-center q-pa-xl text-grey-7">
                    <q-icon name="star" size="3em" />
                    <div class="q-mt-md">Select a favorites list or department from the tree to view details</div>
                  </div>
                </q-card-section>
              </q-card>
            </div>
          </div>

          <div class="row justify-end q-mt-md">
            <q-btn
              color="primary"
              label="Load Favourites"
              icon="cloud_upload"
              @click="loadFavourites"
            />
          </div>
        </div>

        <!-- Load Data Section -->
        <div v-if="activeSection === 'load-data'">
          <div class="text-h5 q-mb-md">Load Data</div>
          <div class="text-body2 text-grey-7 q-mb-lg">
            Upload a directory containing HPDB database files, Favourites, or an entire SD card.
          </div>

          <q-card flat bordered>
            <q-card-section>
              <div class="text-h6 q-mb-sm">
                <q-icon name="folder_open" color="primary" size="sm" class="q-mr-sm" />
                Select Data Directory
              </div>
              <div class="text-body2 q-mb-md">
                Choose one of:
                <ul class="q-my-sm q-pl-md">
                  <li>SD Card root directory</li>
                  <li>HPDB database directory (containing hpdb.cfg and s_*.hpd files)</li>
                  <li>Favourites directory (containing f_list.cfg and f_*.hpd files)</li>
                </ul>
                The system will automatically detect what you've uploaded.
              </div>
              
              <q-file
                ref="importFilePicker"
                v-model="importFiles"
                class="q-mt-md"
                filled
                multiple
                use-chips
                label="Select directory to upload"
                accept=".cfg,.hpd,.avd,.dat,.inf"
                :directory="true"
                :webkitdirectory="true"
              />
              
              <div v-if="importLoading && uploadProgress.totalBytes > 0" class="q-mt-md q-pa-md bg-primary-1 rounded-borders">
                <div class="text-body2 text-weight-medium q-mb-sm">
                  <q-icon name="cloud_upload" color="primary" />
                  Uploading files...
                </div>
                <q-linear-progress
                  :value="uploadProgressPercent / 100"
                  color="primary"
                  class="q-mt-xs"
                />
                <div class="row justify-between q-mt-xs">
                  <div class="text-caption text-grey-7">
                    {{ (uploadProgress.bytesUploaded / 1024 / 1024).toFixed(2) }} MB / {{ (uploadProgress.totalBytes / 1024 / 1024).toFixed(2) }} MB
                  </div>
                  <div class="text-caption text-weight-medium">{{ uploadProgressPercent }}%</div>
                </div>
              </div>
              
              <div v-if="importDetection" class="q-mt-md q-pa-md bg-blue-1 rounded-borders">
                <div class="text-subtitle1 text-weight-medium">
                  <q-icon name="info" color="primary" />
                  Detected: {{ importDetection.description }}
                </div>
                <div class="text-body2 q-mt-xs">
                  {{ importDetection.contains }}
                </div>
                <div class="text-caption text-grey-7 q-mt-xs">
                  {{ importDetection.file_count }} file(s) uploaded
                </div>
              </div>

              <!-- Processing Steps Display -->
              <div v-if="hpdbImportProgress.status !== 'idle'" class="q-mt-md">
                <q-card flat bordered>
                  <q-card-section class="q-pa-md">
                    <div class="text-subtitle1 text-weight-medium q-mb-md">
                      <q-icon name="sync" color="primary" class="rotating" />
                      Import Progress
                    </div>
                    
                    <!-- Step 1: Upload -->
                    <div class="q-mb-md">
                      <div class="row items-center q-mb-xs">
                        <q-icon 
                          :name="hpdbImportProgress.status === 'uploading' ? 'radio_button_checked' : 'check_circle'" 
                          :color="hpdbImportProgress.status === 'uploading' ? 'primary' : 'positive'"
                          size="sm"
                          class="q-mr-sm"
                        />
                        <span class="text-body2 text-weight-medium">
                          Step 1: Upload Files
                        </span>
                        <q-space />
                        <q-badge 
                          v-if="hpdbImportProgress.status !== 'uploading'" 
                          color="positive" 
                          label="Complete"
                        />
                      </div>
                    </div>
                    
                    <!-- Step 2: Processing -->
                    <div class="q-mb-md">
                      <div class="row items-center q-mb-xs">
                        <q-icon 
                          :name="hpdbImportProgress.status === 'processing' ? 'radio_button_checked' : hpdbImportProgress.status === 'completed' ? 'check_circle' : 'radio_button_unchecked'" 
                          :color="hpdbImportProgress.status === 'processing' ? 'primary' : hpdbImportProgress.status === 'completed' ? 'positive' : 'grey'"
                          size="sm"
                          class="q-mr-sm"
                        />
                        <span class="text-body2 text-weight-medium">
                          Step 2: Process Data
                        </span>
                        <q-space />
                        <q-badge 
                          v-if="hpdbImportProgress.status === 'completed'" 
                          color="positive" 
                          label="Complete"
                        />
                        <q-badge 
                          v-else-if="hpdbImportProgress.status === 'processing'" 
                          color="primary" 
                          :label="`${hpdbImportProgress.processedFiles}/${hpdbImportProgress.totalFiles}`"
                        />
                      </div>
                      
                      <!-- Processing Details -->
                      <div v-if="hpdbImportProgress.status === 'processing'" class="q-ml-lg q-pl-sm">
                        <div v-if="hpdbImportProgress.stage" class="text-caption text-grey-7 q-mb-xs">
                          Stage: {{ hpdbImportProgress.stage }}
                        </div>
                        <div v-if="hpdbImportProgress.message" class="text-caption text-weight-medium q-mb-sm text-primary">
                          {{ hpdbImportProgress.message }}
                        </div>
                        <div v-if="hpdbImportProgress.currentFile" class="text-caption text-grey-7 q-mb-sm">
                          File: {{ hpdbImportProgress.currentFile }}
                        </div>
                        <q-linear-progress
                          :value="hpdbImportProgressPercent"
                          color="primary"
                          class="q-mb-xs"
                          stripe
                        />
                        <div class="text-caption text-grey-7">
                          {{ hpdbImportProgress.processedFiles }} / {{ hpdbImportProgress.totalFiles }} files
                          <span v-if="hpdbImportProgress.currentRecords">
                            ({{ hpdbImportProgress.currentRecords }} / {{ hpdbImportProgress.totalRecords }} records)
                          </span>
                        </div>
                      </div>
                    </div>
                    
                    <!-- Info Message -->
                    <div v-if="hpdbImportProgress.status === 'processing'" class="q-pa-sm bg-blue-1 rounded-borders">
                      <q-icon name="info" color="primary" size="xs" />
                      <span class="text-caption text-grey-8 q-ml-xs">
                        Safe to navigate away - processing continues in background
                      </span>
                    </div>
                  </q-card-section>
                </q-card>
              </div>
            </q-card-section>
            
            <q-card-actions>
              <q-btn
                outline
                color="primary"
                label="Choose Directory"
                icon="folder_open"
                @click="openImportPicker"
              />
              <q-btn
                outline
                color="primary"
                label="Analyze & Upload"
                icon="upload"
                :loading="importLoading"
                :disable="!hasImportFiles"
                @click="analyzeImport"
              />
              <q-space />
              <q-btn
                outline
                color="primary"
                label="Clean Temp Uploads"
                icon="delete_sweep"
                @click="cleanupTempUploads"
              />
              <q-btn
                outline
                color="primary"
                label="Re-Parse Data from Last Upload"
                :loading="hpdbImportLoading"
                @click="reloadHpdbFromRaw"
              />
              <q-btn
                outline
                color="primary"
                label="Export Favourites Folder"
                icon="file_download"
                @click="exportFavoritesFolder"
              />
              <q-btn
                outline
                color="warning"
                label="Clear Raw Data"
                @click="clearRawDataConfirm"
              />
              <q-btn
                outline
                color="negative"
                label="Cancel Import & Clear Queue"
                @click="cancelImportConfirm"
              />
              <q-btn
                outline
                color="negative"
                label="Clear All Data"
                @click="clearHpdbDataConfirm"
              />
            </q-card-actions>
          </q-card>
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

    <!-- Add Channel Dialog -->
    <q-dialog v-model="showAddChannelDialog">
      <q-card style="min-width: 500px">
        <q-card-section class="row items-center q-pb-none">
          <div class="text-h6">Add Channel</div>
          <q-space />
          <q-btn icon="close" flat round dense @click="showAddChannelDialog = false" />
        </q-card-section>

        <q-card-section class="q-pt-none" style="max-height: 600px; overflow-y: auto;">
          <!-- Basic Info -->
          <div class="text-subtitle2 q-mb-md">Basic Information</div>
          <q-input
            v-model="newChannel.name_tag"
            label="Channel Name (NameTag)"
            hint="Max 64 characters"
            maxlength="64"
            counter
            class="q-mb-md"
          />
          <q-input
            v-model.number="newChannel.frequency"
            label="Frequency (Hz)"
            type="number"
            hint="Enter frequency in Hz"
            class="q-mb-md"
          />
          <q-select
            v-model="newChannel.modulation"
            :options="['FM', 'NFM', 'AM', 'AUTO']"
            label="Modulation"
            class="q-mb-md"
          />

          <!-- Sub-Audio Options -->
          <div class="text-subtitle2 q-mb-md q-mt-lg">Sub-Audio Options</div>
          <q-input
            v-model="newChannel.audio_option"
            label="Audio Option"
            hint="e.g., TONE=67.0, NAC=293, ColorCode=1, RAN=12, Area=2"
            class="q-mb-md"
          />

          <!-- Attenuator & Delay -->
          <div class="text-subtitle2 q-mb-md q-mt-lg">Signal Settings</div>
          <q-select
            v-model="newChannel.attenuator"
            :options="['Off', 'On']"
            label="Attenuator"
            class="q-mb-md"
          />
          <q-select
            v-model.number="newChannel.delay"
            :options="[30, 10, 5, 4, 3, 2, 1, 0, -5, -10]"
            label="Delay (seconds)"
            class="q-mb-md"
          />
          <q-select
            v-model.number="newChannel.volume_offset"
            :options="['-3', '-2', '-1', '0', '1', '2', '3']"
            label="Volume Offset (dB)"
            class="q-mb-md"
          />

          <!-- Alert Settings -->
          <div class="text-subtitle2 q-mb-md q-mt-lg">Alert Settings</div>
          <q-select
            v-model="newChannel.alert_tone"
            :options="['Off', '1', '2', '3', '4', '5', '6', '7', '8', '9']"
            label="Alert Tone"
            class="q-mb-md"
          />
          <q-select
            v-model="newChannel.alert_light"
            :options="['Off', 'On']"
            label="Alert Light"
            class="q-mb-md"
          />

          <!-- Priority & Flags -->
          <div class="text-subtitle2 q-mb-md q-mt-lg">Flags & Priority</div>
          <q-select
            v-model="newChannel.p_ch"
            :options="['Off', 'On']"
            label="P-CH (Priority Channel)"
            class="q-mb-md"
          />
          <q-input
            v-model.number="newChannel.number_tag"
            label="Number Tag"
            type="number"
            hint="Off or 0-999"
            class="q-mb-md"
          />
          <q-input
            v-model.number="newChannel.priority"
            label="Priority Channel"
            type="number"
            hint="0 = no priority"
            class="q-mb-md"
          />

          <!-- Enabled -->
          <div class="text-subtitle2 q-mb-md q-mt-lg">Status</div>
          <q-toggle
            v-model="newChannel.enabled"
            label="Enabled"
            class="q-mb-md"
          />
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancel" @click="showAddChannelDialog = false" />
          <q-btn
            flat
            label="Add Channel"
            color="primary"
            @click="addChannelToFavorites"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Add Department Dialog -->
    <q-dialog v-model="showAddDepartmentDialog">
      <q-card style="min-width: 500px">
        <q-card-section class="row items-center q-pb-none">
          <div class="text-h6">Add Department</div>
          <q-space />
          <q-btn icon="close" flat round dense @click="showAddDepartmentDialog = false" />
        </q-card-section>

        <q-card-section class="q-pt-none" style="max-height: 600px; overflow-y: auto;">
          <!-- Basic Info -->
          <div class="text-subtitle2 q-mb-md">Basic Information</div>
          <q-input
            v-model="newDepartment.name_tag"
            label="Department Name (NameTag)"
            hint="Max 255 characters"
            maxlength="255"
            counter
            class="q-mb-md"
          />

          <!-- Location Info -->
          <div class="text-subtitle2 q-mb-md q-mt-lg">Location Information</div>
          <q-select
            v-model="newDepartment.location_type"
            :options="['Conventional', 'Trunked', 'Other']"
            label="Location Type"
            class="q-mb-md"
          />
          <q-input
            v-model.number="newDepartment.latitude"
            label="Latitude"
            type="number"
            step="0.00001"
            hint="Optional"
            class="q-mb-md"
          />
          <q-input
            v-model.number="newDepartment.longitude"
            label="Longitude"
            type="number"
            step="0.00001"
            hint="Optional"
            class="q-mb-md"
          />
          <q-input
            v-model.number="newDepartment.range_miles"
            label="Range (miles)"
            type="number"
            hint="Optional"
            class="q-mb-md"
          />

          <!-- Other Settings -->
          <div class="text-subtitle2 q-mb-md q-mt-lg">Settings</div>
          <q-toggle
            v-model="newDepartment.enabled"
            label="Enabled"
            class="q-mb-md"
          />
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancel" @click="showAddDepartmentDialog = false" />
          <q-btn
            flat
            label="Add Department"
            color="primary"
            @click="addDepartmentToFavorites"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Edit Favorites List Dialog -->
    <q-dialog v-model="showEditFavoritesDialog">
      <q-card style="min-width: 400px">
        <q-card-section class="row items-center q-pb-none">
          <div class="text-h6">Edit Favorites List Name</div>
          <q-space />
          <q-btn icon="close" flat round dense @click="showEditFavoritesDialog = false" />
        </q-card-section>

        <q-card-section>
          <q-input
            v-model="editingFavorites.user_name"
            label="Favorites List Name"
            hint="Display name only (filename unchanged)"
            maxlength="255"
            counter
          />
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancel" @click="showEditFavoritesDialog = false" />
          <q-btn
            flat
            label="Save"
            color="primary"
            @click="updateFavoritesList"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Edit Department Dialog -->
    <q-dialog v-model="showEditDepartmentDialog">
      <q-card style="min-width: 400px">
        <q-card-section class="row items-center q-pb-none">
          <div class="text-h6">Edit Department Name</div>
          <q-space />
          <q-btn icon="close" flat round dense @click="showEditDepartmentDialog = false" />
        </q-card-section>

        <q-card-section>
          <q-input
            v-model="editingDepartment.name_tag"
            label="Department Name"
            maxlength="255"
            counter
          />
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancel" @click="showEditDepartmentDialog = false" />
          <q-btn
            flat
            label="Save"
            color="primary"
            @click="updateDepartment"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Edit Channel Dialog -->
    <q-dialog v-model="showEditChannelDialog">
      <q-card style="min-width: 400px">
        <q-card-section class="row items-center q-pb-none">
          <div class="text-h6">Edit Channel Name</div>
          <q-space />
          <q-btn icon="close" flat round dense @click="showEditChannelDialog = false" />
        </q-card-section>

        <q-card-section>
          <q-input
            v-model="editingChannel.name_tag"
            label="Channel Name"
            maxlength="64"
            counter
          />
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancel" @click="showEditChannelDialog = false" />
          <q-btn
            flat
            label="Save"
            color="primary"
            @click="updateChannel"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Import Confirmation Dialog -->
    <q-dialog v-model="showImportConfirm" persistent>
      <q-card style="min-width: 500px">
        <q-card-section class="row items-center q-pb-none">
          <div class="text-h6">Confirm Data Import</div>
          <q-space />
          <q-btn icon="close" flat round dense @click="closeImportDialog" />
        </q-card-section>

        <q-card-section v-if="importDetection">
          <div class="text-body1 q-mb-md">
            <q-icon name="folder" color="primary" size="md" class="q-mr-sm" />
            <strong>{{ importDetection.description }}</strong>
          </div>
          
          <div class="text-body2 q-mb-md">
            Contains: {{ importDetection.contains }}
          </div>

          <div class="q-pa-md bg-orange-1 rounded-borders">
            <div class="text-body2 text-weight-medium q-mb-sm">
              <q-icon name="warning" color="warning" />
              What data will be affected?
            </div>
            <div class="text-body2" v-if="importDetection.type === 'hpdb'">
              This will import HPDB database records (countries, states, counties, agencies, and frequencies).
            </div>
            <div class="text-body2" v-else-if="importDetection.type === 'favorites'">
              This will import favourites profiles and channel configurations.
            </div>
            <div class="text-body2" v-else-if="importDetection.type === 'sd_card'">
              This will import both HPDB database AND favourites profiles from your SD card.
            </div>
          </div>

          <div class="q-mt-md text-body2 text-grey-7">
            <strong>Choose import mode:</strong>
            <ul class="q-my-sm q-pl-md">
              <li><strong>Replace:</strong> Clear existing data and import fresh</li>
              <li><strong>Merge:</strong> Add to existing data (duplicates may occur)</li>
            </ul>
          </div>
        </q-card-section>

        <q-card-actions align="right" class="q-pa-md">
          <q-btn flat label="Cancel" @click="closeImportDialog" />
          <q-btn
            outline
            label="Proceed with Merge"
            color="primary"
            icon="merge_type"
            @click="confirmImport('merge')"
            :loading="importLoading"
          />
          <q-btn
            unelevated
            label="Proceed with Replace"
            color="primary"
            icon="refresh"
            @click="confirmImport('replace')"
            :loading="importLoading"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Favourites Import Dialog -->
    <q-dialog v-model="showFavoritesImportDialog" persistent>
      <q-card style="min-width: 520px">
        <q-card-section class="row items-center q-pb-none">
          <div class="text-h6">Load Favourites</div>
          <q-space />
          <q-btn icon="close" flat round dense @click="closeFavoritesImportDialog" />
        </q-card-section>

        <q-card-section>
          <div class="text-body2 q-mb-md">
            Upload a favourites directory containing f_list.cfg and f_*.hpd files.
          </div>

          <q-file
            ref="favoritesImportFilePicker"
            v-model="favoritesImportFiles"
            class="q-mt-md"
            filled
            multiple
            use-chips
            label="Select favourites directory (f_list.cfg + f_*.hpd files)"
            accept=".cfg,.hpd"
            :directory="true"
            :webkitdirectory="true"
          />

          <div v-if="favoritesImportLoading && favoritesUploadProgress.totalBytes > 0" class="q-mt-md q-pa-md bg-primary-1 rounded-borders">
            <div class="text-body2 text-weight-medium q-mb-sm">
              <q-icon name="cloud_upload" color="primary" />
              Uploading and importing files...
            </div>
            <q-linear-progress
              :value="favoritesUploadProgressPercent / 100"
              color="primary"
              class="q-mt-xs"
            />
            <div class="row justify-between q-mt-xs">
              <div class="text-caption text-grey-7">
                {{ (favoritesUploadProgress.bytesUploaded / 1024 / 1024).toFixed(2) }} MB /
                {{ (favoritesUploadProgress.totalBytes / 1024 / 1024).toFixed(2) }} MB
              </div>
              <div class="text-caption text-weight-medium">{{ favoritesUploadProgressPercent }}%</div>
            </div>
          </div>

          <div class="q-mt-md q-pa-md bg-orange-1 rounded-borders">
            <div class="text-caption text-weight-medium text-orange-9">
              <q-icon name="warning" color="orange" />
              <strong>Warning:</strong> Importing will overwrite all existing favourites data.
            </div>
          </div>
        </q-card-section>

        <q-card-actions align="right" class="q-pa-md">
          <q-btn flat label="Cancel" @click="closeFavoritesImportDialog" />
          <q-btn
            outline
            label="Browse Files"
            color="primary"
            icon="folder_open"
            @click="openFavoritesImportPicker"
            :disable="favoritesImportLoading"
          />
          <q-btn
            unelevated
            label="Import & Replace"
            color="primary"
            icon="upload"
            :loading="favoritesImportLoading"
            :disable="!favoritesHasImportFiles"
            @click="confirmFavoritesImport"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Channel Group Map Dialog -->
    <ChannelGroupMapDialog 
      v-model="showChannelGroupMap"
      :channel-group="mapChannelGroup"
    />
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
import ChannelGroupMapDialog from '../components/ChannelGroupMapDialog.vue'

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
const selectedChannelGroup = ref(null)
const countyAgencies = ref([])
const agencyTreeNodes = ref([])
const agencyFrequencies = ref([])
const agencyChannelGroups = ref([])
const channelGroupFrequencies = ref([])
const loadingAgencies = ref(false)
const loadingFrequencies = ref(false)
const showChannelGroupMap = ref(false)
const mapChannelGroup = ref(null)

const frequencyColumns = [
  { name: 'channel_name', label: 'Channel Name', field: row => row.name_tag || row.description || '', align: 'left', sortable: true },
  { name: 'avoid', label: 'Avoid', field: row => (!row.enabled ? 'Yes' : 'No'), align: 'center', sortable: true },
  { name: 'frequency', label: 'Frequency', field: 'frequency', align: 'left', sortable: true },
  { name: 'modulation', label: 'Modulation', field: 'modulation', align: 'left', sortable: true },
  { name: 'audio_option', label: 'Audio Option', field: 'audio_option', align: 'left', sortable: true },
  { name: 'service_type', label: 'Service Type', field: 'description', align: 'left', sortable: true },
  { name: 'attenuator', label: 'Attenuator', field: 'attenuator', align: 'center' },
  { name: 'delay', label: 'Delay', field: 'delay', align: 'center', sortable: true },
  { name: 'alert_tone', label: 'Alert Tone', field: 'alert_tone', align: 'left' },
  { name: 'alert_light', label: 'Alert Light', field: 'alert_light', align: 'left' },
  { name: 'volume_offset', label: 'Volume Offset', field: 'volume_offset', align: 'center' },
  { name: 'number_tag', label: 'Number Tag', field: 'number_tag', align: 'center' },
  { name: 'p_ch', label: 'P-CH', field: 'p_ch', align: 'center' }
]

const channelGroupColumns = [
  { name: 'system_name', label: 'System Name', field: 'name_tag', align: 'left', sortable: true },
  { name: 'avoid', label: 'Avoid', field: row => (!row.enabled ? 'Yes' : 'No'), align: 'center', sortable: true },
  { name: 'system_type', label: 'System Type', field: 'location_type', align: 'left', sortable: true },
  { name: 'latitude', label: 'Latitude', field: 'latitude', align: 'center', sortable: true },
  { name: 'longitude', label: 'Longitude', field: 'longitude', align: 'center', sortable: true },
  { name: 'range_miles', label: 'Range (mi)', field: 'range_miles', align: 'center', sortable: true },
  { name: 'frequency_count', label: 'Frequencies', field: 'frequency_count', align: 'center', sortable: true }
]

const agencyColumns = [
  { name: 'system_name', label: 'System Name', field: 'name_tag', align: 'left', sortable: true },
  { name: 'avoid', label: 'Avoid', field: row => (!row.enabled ? 'Yes' : 'No'), align: 'center', sortable: true },
  { name: 'system_type', label: 'System Type', field: 'system_type', align: 'left', sortable: true },
  { name: 'id_search', label: 'ID:Search', field: 'trunk_id_search', align: 'left', sortable: true },
  { name: 'emergency_alert', label: 'Emergency Alert', field: 'emergency_alert', align: 'center' },
  { name: 'emergency_alert_light', label: 'Emergency Alert Light', field: 'trunk_emergency_alert_light', align: 'center' },
  { name: 'status_bit', label: 'Status Bit', field: 'trunk_status_bit', align: 'center' },
  { name: 'quick_key', label: 'Quick Key', field: 'quick_key', align: 'center' },
  { name: 'number_tag', label: 'Number Tag', field: 'number_tag', align: 'center' },
  { name: 'hold_time', label: 'Hold Time', field: 'hold_time', align: 'center' },
  { name: 'priority_id_scan', label: 'Priority ID Scan', field: 'priority_id_scan', align: 'center' },
  { name: 'end_code', label: 'End Code', field: 'trunk_end_code', align: 'left', sortable: true },
  { name: 'nxdn_format', label: 'NXDN TGID Format', field: 'trunk_nxdn_format', align: 'left', sortable: true },
  { name: 'agc_analog', label: 'Analog AGC', field: 'agc_analog', align: 'center' },
  { name: 'agc_digital', label: 'Digital AGC', field: 'agc_digital', align: 'center' }
]

// Favourites
const favorites = ref([])
const favoritesLoading = ref(false)
const selectedFavoritesNodeId = ref(null)
const selectedFavoritesNode = ref(null)
const selectedFavoritesList = ref(null)
const favoritesColumns = [
  { name: 'user_name', label: 'User Name', field: 'user_name', align: 'left', sortable: true },
  { name: 'filename', label: 'Filename', field: 'filename', align: 'left', sortable: true },
  { name: 'location_control', label: 'Location Control', field: 'location_control', align: 'center', sortable: true },
  { name: 'monitor', label: 'Monitor', field: 'monitor', align: 'center', sortable: true },
  { name: 'quick_key', label: 'Quick Key', field: 'quick_key', align: 'center', sortable: true },
  { name: 'number_tag', label: 'Number Tag', field: 'number_tag', align: 'center', sortable: true },
  { name: 'startup_keys', label: 'Startup Keys', field: row => {
    if (!row.startup_keys || !Array.isArray(row.startup_keys)) return 'None';
    const onKeys = row.startup_keys.map((val, idx) => val === 'On' ? idx : null).filter(x => x !== null);
    return onKeys.length > 0 ? onKeys.join(', ') : 'None';
  }, align: 'center' }
]

const favoritesChannelColumns = [
  { name: 'name_tag', label: 'Channel Name', field: 'name_tag', align: 'left', sortable: true },
  { name: 'frequency', label: 'Frequency', field: 'frequency', align: 'left', sortable: true },
  { name: 'modulation', label: 'Modulation', field: 'modulation', align: 'left', sortable: true },
  { name: 'audio_option', label: 'Audio Option', field: 'audio_option', align: 'left', sortable: true },
  { name: 'delay', label: 'Delay', field: 'delay', align: 'center', sortable: true },
  { name: 'alert_tone', label: 'Alert Tone', field: 'alert_tone', align: 'center' },
  { name: 'alert_light', label: 'Alert Light', field: 'alert_light', align: 'center' },
  { name: 'enabled', label: 'Enabled', field: 'enabled', align: 'center' },
  { name: 'actions', label: 'Actions', field: 'actions', align: 'center' }
]

const favoritesListDepartmentColumns = [
  { name: 'name_tag', label: 'Department Name', field: 'name_tag', align: 'left', sortable: true },
  { name: 'enabled', label: 'Enabled', field: 'enabled', align: 'center', sortable: true },
  { name: 'freq_count', label: 'Channels', field: 'freq_count', align: 'center', sortable: true },
  { name: 'location_type', label: 'Location Type', field: 'location_type', align: 'left', sortable: true },
  { name: 'latitude', label: 'Latitude', field: 'latitude', align: 'center', sortable: true },
  { name: 'longitude', label: 'Longitude', field: 'longitude', align: 'center', sortable: true },
  { name: 'range_miles', label: 'Range (mi)', field: 'range_miles', align: 'center', sortable: true },
  { name: 'actions', label: 'Actions', field: 'actions', align: 'center' }
]

const favoritesTreeNodes = computed(() => {
  console.log('[favoritesTreeNodes] Computing tree nodes, favorites.value:', favorites.value)
  
  const favoritesList = favorites.value.map((fav, idx) => {
    console.log(`[favoritesTreeNodes] Processing favorite #${idx}: ${fav.user_name}, has groups?`, !!fav.groups, 'groups count:', fav.groups?.length || 0)
    
    return {
      id: `fav_${fav.id}`,
      label: `${fav.user_name} (${fav.filename})`,
      type: 'favorites_list',
      favData: fav,
      children: fav.groups ? fav.groups.map((group, gIdx) => ({
        id: `dept_${fav.id}_${gIdx}`,
        label: `${group.name_tag || `Department ${gIdx + 1}`} (${group.freq_count || 0})`,
        type: 'department',
        system_type: group.system_type,
        favId: fav.id,
        groupId: group.id,
        channel_count: group.freq_count,
        groupData: group
      })) : []
    }
  })
  
  console.log('[favoritesTreeNodes] Computed list has', favoritesList.length, 'items')
  
  // Wrap all favorites in a top-level "Favourites" node
  const result = [{
    id: 'favorites_root',
    label: 'Favourites',
    type: 'root',
    children: favoritesList
  }]
  
  console.log('[favoritesTreeNodes] Final tree structure:', result)
  return result
})

const favoritesChannels = computed(() => {
  if (!selectedFavoritesNode.value || !selectedFavoritesNode.value.groupData) return []
  return selectedFavoritesNode.value.groupData.channels || []
})

const showCreateDialog = ref(false)
const showAddChannelDialog = ref(false)
const newChannel = ref({
  name_tag: '',
  description: '',
  frequency: '',
  modulation: 'FM',
  audio_option: '',
  enabled: true,
  delay: 15,
  attenuator: 'Off',
  alert_tone: 'Off',
  alert_light: 'Off',
  volume_offset: '0',
  p_ch: 'Off',
  number_tag: null,
  priority: 0
})

const showAddDepartmentDialog = ref(false)
const newDepartment = ref({
  name_tag: '',
  location_type: 'Conventional',
  latitude: null,
  longitude: null,
  range_miles: null,
  enabled: true
})

const showEditFavoritesDialog = ref(false)
const editingFavorites = ref({
  id: null,
  user_name: ''
})

const showEditDepartmentDialog = ref(false)
const editingDepartment = ref({
  id: null,
  name_tag: ''
})

const showEditChannelDialog = ref(false)
const editingChannel = ref({
  id: null,
  name_tag: ''
})

const importFiles = ref([])
const importFilePicker = ref(null)
const hasImportFiles = computed(() => {
  const files = Array.isArray(importFiles.value)
    ? importFiles.value
    : Array.from(importFiles.value || [])
  return files.length > 0
})
const importDetection = ref(null)
const importSession = ref(null)
const importTempPath = ref(null)
const importFocus = ref(null)
const showImportConfirm = ref(false)
const importLoading = ref(false)
const uploadProgress = ref({
  bytesUploaded: 0,
  totalBytes: 0,
  percent: 0
})
const uploadProgressPercent = computed(() => uploadProgress.value.percent)

const favoritesImportFiles = ref([])
const favoritesImportFilePicker = ref(null)
const favoritesHasImportFiles = computed(() => {
  const files = Array.isArray(favoritesImportFiles.value)
    ? favoritesImportFiles.value
    : Array.from(favoritesImportFiles.value || [])
  return files.length > 0
})
const favoritesImportDetection = ref(null)
const favoritesImportSession = ref(null)
const favoritesImportTempPath = ref(null)
const showFavoritesImportDialog = ref(false)
const favoritesImportLoading = ref(false)
const favoritesUploadProgress = ref({
  bytesUploaded: 0,
  totalBytes: 0,
  percent: 0
})
const favoritesUploadProgressPercent = computed(() => favoritesUploadProgress.value.percent)
const newProfile = ref({
  name: '',
  model: '',
  firmware_version: ''
})

onMounted(async () => {
  // Check for section query parameter
  const section = route.query.section
  if (section && ['home', 'database', 'favorites'].includes(section)) {
    activeSection.value = section
  }
  
  // Check for ongoing import job from previous session
  const storedJobId = localStorage.getItem('hpdb_import_job_id')
  const storedTimestamp = localStorage.getItem('hpdb_import_timestamp')
  
  if (storedJobId && storedTimestamp) {
    const jobAge = Date.now() - parseInt(storedTimestamp)
    // Only resume if job is less than 24 hours old
    if (jobAge < 86400000) {
      console.log('Resuming import job:', storedJobId)
      // Automatically switch to load-data section to show progress
      activeSection.value = 'load-data'
      // Set initial progress state
      hpdbImportProgress.value = {
        status: 'processing',
        stage: 'Resuming import...',
        currentFile: '',
        processedFiles: 0,
        totalFiles: 0
      }
      // Start polling the existing job
      startHpdbImportPolling(storedJobId)
    } else {
      // Job is too old, clear it
      localStorage.removeItem('hpdb_import_job_id')
      localStorage.removeItem('hpdb_import_timestamp')
    }
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
      api.get('/hpdb/stats/'),
      api.get('/usersettings/stats/')
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
    const { data } = await api.get('/hpdb/tree/tree/')
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
    const { data } = await api.get(`/hpdb/channel-groups/?agency=${numericId}`)
    // Handle paginated response
    const groups = data.results || []
    return groups.map(group => ({
      id: `group-${group.id}`,
      type: 'group',
      name_tag: group.name_tag,
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
    let favList = Array.isArray(data) ? data : (data.results || [])
    console.log('[DEBUG] Loaded', favList.length, 'favorites from API')
    
    // Sort by filename
    favList.sort((a, b) => (a.filename || '').localeCompare(b.filename || ''))
    
    // Load detailed info (groups/channels) for each favorite
    const favListsWithDetails = await Promise.all(
      favList.map(async (fav) => {
        try {
          const { data: detailData } = await api.get(`/usersettings/favorites-lists/${fav.id}/detail/`)
          const merged = { ...fav, ...detailData }
          console.log('[DEBUG] Loaded details for', fav.user_name, '- groups:', merged.groups?.length || 0)
          return merged
        } catch (err) {
          console.error(`Error loading details for favorite ${fav.id}:`, err)
          return fav
        }
      })
    )
    
    console.log('[DEBUG] Final favorites with details:', favListsWithDetails.length)
    favorites.value = favListsWithDetails
    console.log('[DEBUG] Set favorites.value, tree nodes count:', favoritesTreeNodes.value.length)
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

const selectFavoritesNode = async (node) => {
  selectedFavoritesNode.value = node
  selectedFavoritesNodeId.value = node.id
  
  if (node.type === 'department') {
    // Find the parent favorites list
    const favId = node.favId
    selectedFavoritesList.value = favorites.value.find(f => f.id === favId)
    
    // Fetch frequencies or TGIDs for this department
    try {
      const groupId = node.groupId
      const systemType = node.system_type
      
      console.log('[selectFavoritesNode] Loading channels for:', node.label, 'groupId:', groupId, 'systemType:', systemType)
      
      if (systemType === 'Conventional') {
        const { data } = await api.get(`/usersettings/cgroups/${groupId}/`)
        // Store frequencies in the node's groupData
        node.groupData.channels = data.frequencies || []
        console.log('[selectFavoritesNode] Loaded', data.frequencies?.length || 0, 'frequencies')
      } else if (systemType === 'Trunked') {
        const { data } = await api.get(`/usersettings/tgroups/${groupId}/`)
        // Store TGIDs as channels in the node's groupData
        node.groupData.channels = (data.tgids || []).map(tgid => ({
          id: tgid.id,
          name_tag: tgid.name_tag,
          frequency: tgid.tgid,  // Use TGID value as "frequency" for display
          modulation: tgid.audio_type,
          avoid: tgid.avoid,
          delay: tgid.delay,
          volume_offset: tgid.volume_offset,
          alert_tone: tgid.alert_tone,
          alert_volume: tgid.alert_volume,
          enabled: tgid.avoid !== 'On'
        }))
        console.log('[selectFavoritesNode] Loaded', data.tgids?.length || 0, 'TGIDs')
      }
    } catch (error) {
      console.error('[selectFavoritesNode] Error loading channels:', error)
      $q.notify({ type: 'negative', message: 'Failed to load channels' })
    }
  } else if (node.type === 'favorites_list') {
    // Set the favorites list directly
    selectedFavoritesList.value = node.favData
  }
}

const getFavoritesNodeIcon = (node) => {
  switch (node.type) {
    case 'root': return 'star'
    case 'favorites_list': return 'bookmark'
    case 'department': return 'radio'
    default: return 'circle'
  }
}

const getFavoritesNodeColor = (node) => {
  switch (node.type) {
    case 'root': return 'amber'
    case 'favorites_list': return 'orange'
    case 'department': return 'blue'
    default: return 'grey'
  }
}

const selectCounty = async (node) => {
  selectedCounty.value = node
  selectedAgency.value = null
  selectedChannelGroup.value = null
  agencyFrequencies.value = []
  channelGroupFrequencies.value = []
  agencyTreeNodes.value = []
  loadingAgencies.value = true
  countyAgencies.value = []
  
  try {
    // Extract numeric ID from node ID (e.g., "county-268" -> "268")
    const numericId = node.id.toString().replace('county-', '')
    
    // Load agencies for this county
    const { data: agenciesResponse } = await api.get(`/hpdb/tree/agencies/?county=county-${numericId}`)
    countyAgencies.value = agenciesResponse
    
    // Build tree nodes: agencies with channel groups as children
    agencyTreeNodes.value = agenciesResponse.map(agency => ({
      id: agency.id.toString().startsWith('agency-') ? agency.id.toString() : `agency-${agency.id}`,
      type: 'agency',
      name_tag: agency.name_tag,
      system_type: agency.system_type,
      enabled: agency.enabled,
      group_count: agency.group_count || 0,
      lazy: true  // Will load children on expand
    }))
    
    console.log('Agency tree nodes built:', agencyTreeNodes.value)
  } catch (error) {
    console.error('Error loading county agencies:', error)
    $q.notify({ type: 'negative', message: 'Failed to load systems' })
  } finally {
    loadingAgencies.value = false
  }
}

const onAgencyLazyLoad = async ({ node, key, done, fail }) => {
  console.log('[LAZY-LOAD] Triggered for node:', { node, key })
  console.log('[LAZY-LOAD] Node type:', node.type)
  console.log('[LAZY-LOAD] Node id:', node.id)
  
  // Load channel groups when agency node is expanded
  if (node.type === 'agency') {
    try {
      const numericId = node.id.toString().replace(/^(agency-)+/, '')
      console.log('[LAZY-LOAD] Extracted numeric ID:', numericId)
      
      // Only pass agency parameter - no need for county/state since agency is already scoped
      const params = new URLSearchParams()
      params.append('agency', `agency-${numericId}`)
      
      const url = `/hpdb/channel-groups/?${params.toString()}`
      console.log('[LAZY-LOAD] Fetching from URL:', url)
      
      const response = await api.get(url)
      console.log('[LAZY-LOAD] Got response:', response)
      
      const groupsResponse = response.data
      console.log('[LAZY-LOAD] Response data:', groupsResponse)
      
      const groups = Array.isArray(groupsResponse) ? groupsResponse : (groupsResponse.results || [])
      console.log('[LAZY-LOAD] Parsed', groups.length, 'groups from response')
      console.log('[LAZY-LOAD] Groups:', groups)
      
      const groupNodes = groups.map(group => {
        console.log('[LAZY-LOAD] Processing group:', group)
        return {
          id: `cgroup-${group.id}`,
          type: 'group',
          name_tag: group.name_tag,
          enabled: group.enabled,
          latitude: group.latitude,
          longitude: group.longitude,
          range_miles: group.range_miles,
          lazy: false
        }
      })
      
      console.log('[LAZY-LOAD] Created', groupNodes.length, 'group nodes:', groupNodes)
      console.log('[LAZY-LOAD] Calling done() callback with nodes')
      
      done(groupNodes)
      
      console.log('[LAZY-LOAD] done() callback completed successfully')
    } catch (error) {
      console.error('[LAZY-LOAD] ERROR:', error)
      console.error('[LAZY-LOAD] Error message:', error.message)
      console.error('[LAZY-LOAD] Error stack:', error.stack)
      console.log('[LAZY-LOAD] Calling fail() callback')
      fail()
    }
  } else {
    console.log('[LAZY-LOAD] Node is not an agency, calling done([]) and returning')
    done([])
  }
}

const selectNode = async (node) => {
  console.log('[SELECT-NODE] Clicked on node:', node)
  
  if (node.type === 'county' || node.type === 'statewide') {
    selectedCounty.value = node
    selectedAgency.value = null
    selectedChannelGroup.value = null
    agencyChannelGroups.value = []
    channelGroupFrequencies.value = []
    countyAgencies.value = []
    loadingFrequencies.value = true
    
    // Load agencies for this county
    try {
      const numericId = node.id.toString().replace(/^(county-|statewide-)+/, '')
      console.log('Loading agencies for county:', numericId)
      
      const params = new URLSearchParams()
      params.append('county', `county-${numericId}`)
      
      const { data: agenciesResponse } = await api.get(`/hpdb/agencies/?${params.toString()}`)
      console.log('Agencies response:', agenciesResponse)
      
      const agencies = Array.isArray(agenciesResponse) ? agenciesResponse : (agenciesResponse.results || [])
      countyAgencies.value = agencies
      console.log('Agencies loaded:', agencies.length)
    } catch (error) {
      console.error('Error loading agencies:', error)
      $q.notify({ type: 'negative', message: 'Failed to load agencies' })
    } finally {
      loadingFrequencies.value = false
    }
  } else if (node.type === 'agency') {
    selectedAgency.value = node
    selectedChannelGroup.value = null
    channelGroupFrequencies.value = []
    loadingFrequencies.value = true
    agencyChannelGroups.value = []
    
    try {
      const numericId = node.id.toString().replace(/^(agency-)+/, '')
      console.log('Loading channel groups for agency:', numericId)
      
      const params = new URLSearchParams()
      params.append('agency', `agency-${numericId}`)
      
      const { data: groupsResponse } = await api.get(`/hpdb/channel-groups/?${params.toString()}`)
      console.log('Channel groups response:', groupsResponse)
      
      const groups = Array.isArray(groupsResponse) ? groupsResponse : (groupsResponse.results || [])
      agencyChannelGroups.value = groups
      console.log('Channel groups loaded:', groups.length)
    } catch (error) {
      console.error('Error loading channel groups:', error)
      $q.notify({ type: 'negative', message: 'Failed to load channel groups' })
    } finally {
      loadingFrequencies.value = false
    }
  } else if (node.type === 'group') {
    // Load frequencies for this channel group
    selectedChannelGroup.value = node
    loadingFrequencies.value = true
    channelGroupFrequencies.value = []
    
    try {
      const numericId = node.id.toString().replace('cgroup-', '')
      console.log('Loading frequencies for channel group:', numericId)
      
      const params = new URLSearchParams()
      params.append('channel_group', `cgroup-${numericId}`)
      
      const { data: freqResponse } = await api.get(`/hpdb/frequencies/?${params.toString()}`)
      console.log('Frequencies response:', freqResponse)
      
      const frequencies = Array.isArray(freqResponse) ? freqResponse : (freqResponse.results || [])
      channelGroupFrequencies.value = frequencies
      console.log('Frequencies loaded:', frequencies.length)
    } catch (error) {
      console.error('Error loading frequencies:', error)
      $q.notify({ type: 'negative', message: 'Failed to load frequencies' })
    } finally {
      loadingFrequencies.value = false
    }
  }
}

const onAgencyRowClick = async (evt, row) => {
  console.log('[AGENCY-CLICK] Row clicked:', row)
  
  // Create a node-like object to pass to selectNode
  const agencyNode = {
    id: `agency-${row.id}`,
    type: 'agency',
    name_tag: row.name_tag,
    system_type: row.system_type,
    enabled: row.enabled,
    group_count: row.group_count || 0
  }
  
  // Select this agency node which will load its channel groups
  await selectNode(agencyNode)
}

const onChannelGroupRowClick = async (evt, row) => {
  console.log('[CHANNEL-GROUP-CLICK] Row clicked:', row)
  
  // Create a node-like object to pass to selectNode
  const groupNode = {
    id: `cgroup-${row.id}`,
    type: 'group',
    name_tag: row.name_tag,
    enabled: row.enabled,
    latitude: row.latitude,
    longitude: row.longitude,
    range_miles: row.range_miles
  }
  
  // Select this channel group node which will load its frequencies
  await selectNode(groupNode)
}

const openChannelGroupMap = (channelGroup) => {
  console.log('[OPEN-MAP] Opening map for channel group:', channelGroup)
  mapChannelGroup.value = channelGroup
  showChannelGroupMap.value = true
}

const getNodeIcon = (node) => {
  switch (node.type) {
    case 'country': return 'public'
    case 'state': return 'map'
    case 'county': return 'location_city'
    case 'statewide': return 'language'
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
    case 'statewide': return 'purple'
    case 'agency': return node.enabled ? 'primary' : 'grey'
    case 'group': return 'purple'
    default: return 'grey'
  }
}

const onLazyLoad = async ({ node, key, done, fail }) => {
  console.log('[LAZY-LOAD] Triggered for node:', { node, key })
  console.log('[LAZY-LOAD] Node type:', node.type)
  console.log('[LAZY-LOAD] Node properties:', Object.keys(node))
  
  try {
    if (node.type === 'department') {
      // Load frequencies or TGIDs for this department/group
      const groupId = node.groupId
      const systemType = node.system_type
      
      console.log('[LAZY-LOAD] Loading frequencies for department:', node.label, 'groupId:', groupId, 'systemType:', systemType)
      
      if (systemType === 'Conventional') {
        // Fetch CFreqs for conventional group
        console.log('[LAZY-LOAD] Fetching from:', `/usersettings/cgroups/${groupId}/`)
        const { data } = await api.get(`/usersettings/cgroups/${groupId}/`)
        console.log('[LAZY-LOAD] Got data:', data)
        const freqNodes = (data.frequencies || []).map(freq => ({
          id: `freq_${freq.id}`,
          label: `${freq.name_tag || 'Unnamed'} - ${(freq.frequency / 1000000).toFixed(4)} MHz`,
          type: 'frequency',
          frequency: freq.frequency,
          modulation: freq.modulation,
          avoid: freq.avoid,
          lazy: false
        }))
        console.log('[LAZY-LOAD] Created', freqNodes.length, 'frequency nodes')
        done(freqNodes)
      } else if (systemType === 'Trunked') {
        // Fetch TGIDs for trunk group
        console.log('[LAZY-LOAD] Fetching from:', `/usersettings/tgroups/${groupId}/`)
        const { data } = await api.get(`/usersettings/tgroups/${groupId}/`)
        console.log('[LAZY-LOAD] Got data:', data)
        const tgidNodes = (data.tgids || []).map(tgid => ({
          id: `tgid_${tgid.id}`,
          label: `${tgid.name_tag || 'Unnamed'} - TGID: ${tgid.tgid}`,
          type: 'tgid',
          tgid: tgid.tgid,
          audio_type: tgid.audio_type,
          avoid: tgid.avoid,
          lazy: false
        }))
        console.log('[LAZY-LOAD] Created', tgidNodes.length, 'TGID nodes')
        done(tgidNodes)
      } else {
        console.log('[LAZY-LOAD] Unknown system type:', systemType)
        done([])
      }
    } else if (node.type === 'state') {
      // Load counties for the state
      const { data } = await api.get(`/hpdb/tree/counties/?state=${node.id}`)
      done(data)
    } else if (node.type === 'county' || node.type === 'statewide') {
      // Load agencies for this county or statewide
      const { data: agenciesResponse } = await api.get(`/hpdb/tree/agencies/?county=${node.id}`)
      
      const agencyNodes = agenciesResponse.map(agency => ({
        id: agency.id.toString().startsWith('agency-') ? agency.id.toString() : `agency-${agency.id}`,
        type: 'agency',
        name_tag: agency.name_tag,
        system_type: agency.system_type,
        enabled: agency.enabled,
        group_count: agency.group_count || 0,
        lazy: true
      }))
      
      done(agencyNodes)
    } else if (node.type === 'agency') {
      // Load channel groups for this agency
      const numericId = node.id.toString().replace(/^(agency-)+/, '')
      const params = new URLSearchParams()
      params.append('agency', `agency-${numericId}`)
      
      const { data: groupsResponse } = await api.get(`/hpdb/channel-groups/?${params.toString()}`)
      const groups = Array.isArray(groupsResponse) ? groupsResponse : (groupsResponse.results || [])
      
      const groupNodes = groups.map(group => ({
        id: `cgroup-${group.id}`,
        type: 'group',
        name_tag: group.name_tag,
        enabled: group.enabled,
        latitude: group.latitude,
        longitude: group.longitude,
        range_miles: group.range_miles,
        lazy: false
      }))
      
      done(groupNodes)
    } else {
      done([])
    }
  } catch (error) {
    console.error('[LAZY-LOAD] ERROR:', error)
    fail()
    $q.notify({ type: 'negative', message: 'Failed to load data' })
  }
}

const filterMethod = (node, filter) => {
  const filt = filter.toLowerCase()
  return node.name_tag.toLowerCase().includes(filt)
}

const openAgencyDetail = (node) => {
  // Extract numeric ID from node.id (format is "agency-123")
  const agencyId = node.id.toString().replace('agency-', '')
  router.push(`/database/${agencyId}`)
}

const openChannelGroupDetail = (node) => {
  // Extract numeric ID from node.id (format is "cgroup-123")
  const cgroupId = node.id.toString().replace('cgroup-', '')
  // Could navigate to a channel group detail page if available
  console.log('Opening channel group details:', cgroupId)
  $q.notify({ type: 'info', message: `Channel Group: ${node.name_tag}` })
}

// Import/Export Methods

const openImportPicker = () => {
  triggerFilePicker(importFilePicker)
}

const loadFavourites = () => {
  showFavoritesImportDialog.value = true
}

const openFavoritesImportPicker = () => {
  triggerFilePicker(favoritesImportFilePicker)
}

const analyzeImport = async () => {
  const files = Array.isArray(importFiles.value)
    ? importFiles.value
    : Array.from(importFiles.value || [])
  
  if (files.length === 0) {
    openImportPicker()
    return
  }

  importLoading.value = true
  importDetection.value = null
  uploadProgress.value = { bytesUploaded: 0, totalBytes: 0, percent: 0 }
  
  try {
    // Calculate total bytes
    const totalBytes = files.reduce((sum, file) => sum + file.size, 0)
    uploadProgress.value.totalBytes = totalBytes
    
    const formData = new FormData()
    files.forEach(file => formData.append('files', file))
    
    const { data } = await axios.post(
      api.defaults.baseURL + '/import/detect/',
      formData,
      {
        headers: { 'Content-Type': 'multipart/form-data' },
        onUploadProgress: (progressEvent) => {
          uploadProgress.value.bytesUploaded = progressEvent.loaded
          uploadProgress.value.percent = Math.round((progressEvent.loaded / totalBytes) * 100)
        }
      }
    )

    if (importFocus.value === 'favorites' && data.detection?.type !== 'favorites') {
      $q.notify({
        type: 'negative',
        message: 'Please upload a Favourites directory (f_list.cfg + f_*.hpd files)'
      })
      importDetection.value = null
      importSession.value = null
      importTempPath.value = null
      importFocus.value = null
      return
    }

    importSession.value = data.session_id
    importDetection.value = data.detection
    importTempPath.value = data.temp_path
    showImportConfirm.value = true
    
  } catch (error) {
    $q.notify({ 
      type: 'negative', 
      message: 'Detection failed: ' + (error.response?.data?.error || error.message) 
    })
  } finally {
    importLoading.value = false
  }
}

const analyzeFavoritesImport = async () => {
  // Simplified - just trigger the import directly
  const files = Array.isArray(favoritesImportFiles.value)
    ? favoritesImportFiles.value
    : Array.from(favoritesImportFiles.value || [])

  if (files.length === 0) {
    openFavoritesImportPicker()
    return
  }

  // Check for required files and proceed with import
  await confirmFavoritesImport()
}

const closeImportDialog = () => {
  showImportConfirm.value = false
  importDetection.value = null
  importSession.value = null
  importTempPath.value = null
  importFocus.value = null
}

const closeFavoritesImportDialog = () => {
  showFavoritesImportDialog.value = false
  favoritesImportDetection.value = null
  favoritesImportSession.value = null
  favoritesImportTempPath.value = null
  favoritesImportFiles.value = []
}

const confirmImport = async (mode) => {
  if (!importSession.value || !importDetection.value) {
    $q.notify({ type: 'negative', message: 'Import session expired' })
    return
  }

  if (importFocus.value === 'favorites' && importDetection.value.type !== 'favorites') {
    $q.notify({ type: 'negative', message: 'Only Favourites imports are allowed from this action' })
    closeImportDialog()
    return
  }

  console.log('Starting import process:', { 
    mode, 
    session: importSession.value, 
    type: importDetection.value.type 
  })

  importLoading.value = true
  showImportConfirm.value = false
  
  // Show processing status immediately (files already uploaded during detect)
  hpdbImportProgress.value = {
    status: 'processing',
    stage: 'Processing data (this may take a few minutes for large imports)...',
    currentFile: '',
    processedFiles: 0,
    totalFiles: 0
  }
  
  try {
    console.log('Calling process endpoint...')
    console.log('API baseURL:', api.defaults.baseURL)
    console.log('Full URL will be:', api.defaults.baseURL + '/import/process/')
    console.log('Request data:', {
      session_id: importSession.value,
      mode: mode,
      type: importDetection.value.type,
      temp_path: importTempPath.value
    })
    
    const { data } = await api.post('/import/process/', {
      session_id: importSession.value,
      mode: mode,
      type: importDetection.value.type,
      temp_path: importTempPath.value
    }, {
      timeout: 300000 // 5 minute timeout
    })
    
    console.log('Process response received!')
    console.log('Process response:', data)
    
    // Start polling for progress updates
    if (data.job_id) {
      startImportProgressPolling(data.job_id)
    }
    
    // Handle different import types
    if (data.type === 'hpdb' || (data.type === 'sd_card' && data.results?.hpdb)) {
      const hpdbJobId = data.results?.hpdb?.job_id
      if (hpdbJobId) {
        hpdbImportProgress.value = {
          status: 'processing',
          stage: 'systems',
          currentFile: '',
          processedFiles: 0,
          totalFiles: 0
        }
        startHpdbImportPolling(hpdbJobId)
      }
    }
    
    if (data.type === 'favorites' || (data.type === 'sd_card' && data.results?.favorites)) {
      const favResults = data.type === 'favorites' ? data : data.results.favorites
      if (favResults.errors?.length) {
        $q.notify({ 
          type: 'warning', 
          message: `Favourites imported with ${favResults.errors.length} error(s)` 
        })
      } else {
        $q.notify({ 
          type: 'positive', 
          message: `Imported ${favResults.imported} favourite(s)` 
        })
      }
      await scanner.fetchProfiles()
      await loadFavoritesList()
      
      // If this is favorites-only (not SD card with HPDB), clear progress
      if (data.type === 'favorites') {
        resetHpdbImportProgress()
      }
    }
    
    if (data.type === 'sd_card') {
      $q.notify({ 
        type: 'positive', 
        message: 'SD card import started - processing both HPDB and favourites' 
      })
      await loadHPDBTree()
    }
    
  } catch (error) {
    console.error('Import error:', error)
    console.error('Error details:', {
      message: error.message,
      response: error.response,
      request: error.request,
      config: error.config
    })
    $q.notify({ 
      type: 'negative', 
      message: 'Import failed: ' + (error.response?.data?.error || error.message) 
    })
    // Reset progress on error
    resetHpdbImportProgress()
  } finally {
    console.log('Import finally block')
    importLoading.value = false
    importDetection.value = null
    importSession.value = null
    importTempPath.value = null
    importFocus.value = null
  }
}

const confirmFavoritesImport = async () => {
  const files = Array.isArray(favoritesImportFiles.value)
    ? favoritesImportFiles.value
    : Array.from(favoritesImportFiles.value || [])

  if (files.length === 0) {
    $q.notify({ type: 'negative', message: 'No files selected' })
    return
  }

  // Check for required files (f_list.cfg and at least one f_*.hpd)
  const hasListCfg = files.some(f => f.name.toLowerCase() === 'f_list.cfg')
  const hasHpd = files.some(f => f.name.toLowerCase().endsWith('.hpd'))

  if (!hasListCfg || !hasHpd) {
    $q.notify({
      type: 'negative',
      message: 'Required files missing. Please select f_list.cfg and at least one f_*.hpd file'
    })
    return
  }

  // Ask for confirmation before replacing
  $q.dialog({
    title: 'Confirm Import',
    message: 'This will replace all existing favourites data. Continue?',
    cancel: true,
    persistent: true
  }).onOk(async () => {
    await performFavoritesImport(files)
  })
}

const performFavoritesImport = async (files) => {
  favoritesImportLoading.value = true

  try {
    // First, clear existing data
    console.log('[DEBUG] Clearing existing favorites data...')
    await api.post('/usersettings/clear-data/')
    console.log('[DEBUG] Data cleared')

    // Prepare form data
    const totalBytes = files.reduce((sum, file) => sum + file.size, 0)
    const formData = new FormData()
    files.forEach(file => formData.append('files', file))

    // Upload and import
    console.log('[DEBUG] Starting import upload...')
    const { data } = await axios.post(
      api.defaults.baseURL + '/usersettings/import-files/',
      formData,
      {
        headers: { 'Content-Type': 'multipart/form-data' },
        timeout: 300000,
        onUploadProgress: (progressEvent) => {
          favoritesUploadProgress.value.bytesUploaded = progressEvent.loaded
          favoritesUploadProgress.value.totalBytes = totalBytes
          favoritesUploadProgress.value.percent = Math.round((progressEvent.loaded / totalBytes) * 100)
        }
      }
    )

    console.log('[DEBUG] Import response:', data)

    if (data.errors?.length > 0) {
      $q.notify({
        type: 'warning',
        message: `Imported ${data.imported} file(s) with ${data.errors.length} error(s)`
      })
    } else {
      $q.notify({
        type: 'positive',
        message: `Successfully imported ${data.imported} file(s)`
      })
    }

    // Reload favorites to show imported data
    console.log('[DEBUG] Import complete, reloading favorites...')
    await loadFavoritesList()
    console.log('[DEBUG] Favorites reloaded, tree should now show data')
  } catch (error) {
    console.error('[ERROR] Import failed:', error)
    $q.notify({
      type: 'negative',
      message: 'Import failed: ' + (error.response?.data?.error || error.message)
    })
  } finally {
    favoritesImportLoading.value = false
    closeFavoritesImportDialog()
  }
}

const triggerFilePicker = (pickerRef) => {
  const el = pickerRef?.value?.$el
  const input = el?.querySelector('input[type="file"]')
  input?.click()
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
  // Clear stored job ID when resetting
  localStorage.removeItem('hpdb_import_job_id')
  localStorage.removeItem('hpdb_import_timestamp')
}

const stopHpdbImportPolling = () => {
  if (hpdbImportTimer) {
    clearInterval(hpdbImportTimer)
    hpdbImportTimer = null
  }
}

let importProgressTimer = null

const stopImportProgressPolling = () => {
  if (importProgressTimer) {
    clearInterval(importProgressTimer)
    importProgressTimer = null
  }
}

const startImportProgressPolling = (jobId) => {
  stopImportProgressPolling()
  
  const poll = async () => {
    try {
      const { data } = await api.get('/import/progress/', {
        params: { job_id: jobId }
      })
      
      console.log('Import progress update:', data)
      
      hpdbImportProgress.value = {
        status: data.status || 'processing',
        stage: data.stage || '',
        currentFile: data.current_file || '',
        processedFiles: data.processed_files || 0,
        totalFiles: data.total_files || 0,
        message: data.message || ''
      }

      if (data.hpdb_job_id && !hpdbImportTimer) {
        startHpdbImportPolling(data.hpdb_job_id)
      }
      
      if (data.status === 'completed') {
        stopImportProgressPolling()
        $q.notify({ type: 'positive', message: 'Import completed successfully!' })
        await loadHPDBTree()
        await loadFavoritesList()
        await loadStats()
        await scanner.fetchProfiles()
        setTimeout(resetHpdbImportProgress, 2000)
      } else if (data.status === 'failed') {
        stopImportProgressPolling()
        $q.notify({ type: 'negative', message: `Import failed: ${data.message || 'Unknown error'}` })
        resetHpdbImportProgress()
      }
    } catch (error) {
      console.error('Failed to get import progress:', error)
      if (error?.response?.status === 404) {
        stopImportProgressPolling()
        resetHpdbImportProgress()
      }
      // Continue polling even on error
    }
  }
  
  poll()
  importProgressTimer = setInterval(poll, 1000)
}

const startHpdbImportPolling = (jobId) => {
  stopHpdbImportPolling()
  
  // Store job ID in localStorage for page navigation resilience
  localStorage.setItem('hpdb_import_job_id', jobId)
  localStorage.setItem('hpdb_import_timestamp', Date.now().toString())

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
      console.error('Error polling HPDB import progress:', error)
      if (error?.response?.status === 404) {
        stopHpdbImportPolling()
        resetHpdbImportProgress()
      }
      // Continue polling even on error - the job may still be processing
    }
  }

  poll()
  hpdbImportTimer = setInterval(poll, 1000)
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
    title: 'Clear All Data',
    message: 'This will delete ALL data in the system:\n\n• All HPDB database records (countries, states, counties, agencies, frequencies)\n• All Favourites profiles and channel configurations\n\nThis cannot be undone. Continue?',
    ok: {
      label: 'Delete Everything',
      color: 'negative'
    },
    cancel: true,
    persistent: true
  }).onOk(() => {
    clearAllData()
  })
}

const clearRawDataConfirm = () => {
  $q.dialog({
    title: 'Clear Raw Data',
    message: 'This will delete all uploaded raw files:\n\n• HPDB raw files and lines\n• Scanner configuration raw files and lines\n\nYou can re-import from source files. Continue?',
    ok: {
      label: 'Clear Raw Data',
      color: 'warning'
    },
    cancel: true,
    persistent: true
  }).onOk(() => {
    clearRawData()
  })
}

const clearRawData = async () => {
  try {
    await Promise.all([
      api.post('/hpdb/clear-raw-data/'),
      api.post('/usersettings/clear-raw-data/')
    ])
    $q.notify({ type: 'positive', message: 'Raw data cleared successfully' })
  } catch (error) {
    $q.notify({ type: 'negative', message: 'Failed to clear raw data: ' + (error.response?.data?.error || error.message) })
  }
}

const clearAllData = async () => {
  try {
    await Promise.all([
      api.post('/hpdb/clear-data/'),
      api.post('/usersettings/clear-data/')
    ])
    $q.notify({ type: 'positive', message: 'All data cleared successfully' })
    await loadHPDBTree()
    await loadFavoritesList()
    await loadStats()
  } catch (error) {
    $q.notify({ type: 'negative', message: 'Failed to clear data: ' + (error.response?.data?.error || error.message) })
  }
}

const cancelImportConfirm = () => {
  $q.dialog({
    title: 'Cancel Import & Clear Queue',
    message: 'This will:\n\n• Stop any in-progress imports\n• Clear the job queue\n• Cancel pending processing\n\nContinue?',
    ok: {
      label: 'Cancel & Clear',
      color: 'negative'
    },
    cancel: true,
    persistent: true
  }).onOk(() => {
    cancelImport()
  })
}

const cancelImport = async () => {
  try {
    await api.post('/hpdb/cancel-import/')
    $q.notify({ type: 'positive', message: 'Import cancelled and queue cleared' })
    resetHpdbImportProgress()
  } catch (error) {
    $q.notify({ type: 'negative', message: 'Failed to cancel import: ' + (error.response?.data?.error || error.message) })
  }
}

const cleanupTempUploads = async () => {
  try {
    const { data } = await api.post('/import/cleanup/')
    $q.notify({ 
      type: 'positive', 
      message: data.message || `Cleaned up temporary uploads` 
    })
  } catch (error) {
    $q.notify({ 
      type: 'negative', 
      message: 'Cleanup failed: ' + (error.response?.data?.error || error.message) 
    })
  }
}

const exportFavoritesFolder = async () => {
  try {
    const response = await api.get('/usersettings/export-favorites/', { responseType: 'blob' })
    const blob = new Blob([response.data], { type: 'application/zip' })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = 'favorites_lists_export.zip'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)

    $q.notify({ type: 'positive', message: 'Favourites export started' })
  } catch (error) {
    $q.notify({ type: 'negative', message: 'Export failed: ' + (error.response?.data?.error || error.message) })
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

const createNewFavoritesList = async () => {
  const userName = prompt('Enter Favorites List Name:')
  if (!userName) return
  
  try {
    // Find the highest existing file number
    let maxNum = 0
    favorites.value.forEach(fav => {
      const match = fav.filename.match(/f_(\d+)\.hpd/)
      if (match) {
        const num = parseInt(match[1], 10)
        if (num > maxNum) maxNum = num
      }
    })
    
    // Create filename with next sequential number
    const nextNum = maxNum + 1
    const filename = `f_${String(nextNum).padStart(6, '0')}.hpd`
    
    const response = await api.post('/usersettings/favorites-lists/', {
      user_name: userName,
      filename: filename
    })
    
    $q.notify({ type: 'positive', message: 'Favorites list created successfully!' })
    await loadFavoritesList()
  } catch (error) {
    console.error('Error creating favorites list:', error)
    $q.notify({ type: 'negative', message: 'Failed to create favorites list' })
  }
}

const deleteFavoritesList = () => {
  // Check if a favorites list is selected
  if (!selectedFavoritesNode.value || selectedFavoritesNode.value.type !== 'favorites_list') {
    $q.notify({ type: 'warning', message: 'Please select a favorites list to delete' })
    return
  }
  
  const selectedFav = selectedFavoritesNode.value.favData
  const departmentCount = selectedFav.groups ? selectedFav.groups.length : 0
  let channelCount = 0
  if (selectedFav.groups) {
    selectedFav.groups.forEach(group => {
      channelCount += group.freq_count || 0
    })
  }
  
  // Show confirmation dialog with warning
  $q.dialog({
    title: 'Delete Favorites List',
    message: `<strong style="color: #c41c3b;">⚠️ Warning: This action cannot be undone!</strong><br><br>
              You are about to delete:<br>
              <strong>${selectedFav.user_name}</strong> (${selectedFav.filename})<br><br>
              This will permanently delete:<br>
              • <strong>${departmentCount}</strong> department(s)<br>
              • <strong>${channelCount}</strong> channel(s)<br><br>
              Continue?`,
    html: true,
    ok: {
      label: 'Delete',
      color: 'negative'
    },
    cancel: true,
    persistent: true
  }).onOk(async () => {
    try {
      await api.delete(`/usersettings/favorites-lists/${selectedFav.id}/`)
      $q.notify({ type: 'positive', message: 'Favorites list deleted successfully!' })
      selectedFavoritesNode.value = null
      selectedFavoritesNodeId.value = null
      await loadFavoritesList()
    } catch (error) {
      console.error('Error deleting favorites list:', error)
      $q.notify({ type: 'negative', message: 'Failed to delete favorites list' })
    }
  })
}

const addChannelToFavorites = async () => {
  // Validate frequency is a positive integer (Hz)
  if (!newChannel.frequency || newChannel.frequency <= 0) {
    $q.notify({ type: 'negative', message: 'Frequency must be a positive integer (Hz)' })
    return
  }

  // Validate NameTag is not empty if required
  if (!newChannel.name_tag || newChannel.name_tag.trim() === '') {
    $q.notify({ type: 'negative', message: 'Channel name tag is required' })
    return
  }

  // Validate NameTag length (max 64 characters per spec)
  if (newChannel.name_tag.length > 64) {
    $q.notify({ type: 'negative', message: 'Channel name tag must be 64 characters or less' })
    return
  }

  // Validate modulation is selected
  if (!newChannel.modulation) {
    $q.notify({ type: 'negative', message: 'Modulation must be selected' })
    return
  }

  // Validate number tag if not "Off"
  if (newChannel.number_tag && (newChannel.number_tag < 0 || newChannel.number_tag > 999)) {
    $q.notify({ type: 'negative', message: 'Number tag must be between 0 and 999' })
    return
  }

  // Validate volume offset if selected
  if (newChannel.volume_offset && !['-3', '-2', '-1', '0', '1', '2', '3'].includes(String(newChannel.volume_offset))) {
    $q.notify({ type: 'negative', message: 'Volume offset must be between -3 and +3 dB' })
    return
  }

  try {
    // Get the selected department (channel group)
    if (!selectedFavoritesNode.value || selectedFavoritesNode.value.type !== 'department') {
      $q.notify({ type: 'negative', message: 'Please select a department to add channel to' })
      return
    }

    const channelGroup = selectedFavoritesNode.value.groupData
    if (!channelGroup || !channelGroup.id) {
      $q.notify({ type: 'negative', message: 'Invalid department selected' })
      return
    }

    // Create payload for API
    const payload = {
      name_tag: newChannel.name_tag,
      description: newChannel.description || '',
      frequency: parseInt(newChannel.frequency),
      modulation: newChannel.modulation,
      audio_option: newChannel.audio_option || '',
      delay: newChannel.delay || 15,
      attenuator: newChannel.attenuator || 'Off',
      alert_tone: newChannel.alert_tone || 'Off',
      alert_light: newChannel.alert_light || 'Off',
      volume_offset: newChannel.volume_offset || '0',
      p_ch: newChannel.p_ch || 'Off',
      number_tag: newChannel.number_tag || null,
      priority: newChannel.priority ? 'On' : 'Off',
      enabled: newChannel.enabled ? true : false,
      reserved: 'Off',
      channel_group: channelGroup.id // ForeignKey reference
    }

    // POST to API to create new frequency
    const response = await api.post('/usersettings/frequencies/', payload)
    
    $q.notify({ type: 'positive', message: `Channel "${newChannel.name_tag}" added successfully!` })
    
    // Reset form
    newChannel.name_tag = ''
    newChannel.description = ''
    newChannel.frequency = null
    newChannel.modulation = ''
    newChannel.audio_option = ''
    newChannel.enabled = true
    newChannel.delay = 15
    newChannel.attenuator = 'Off'
    newChannel.alert_tone = 'Off'
    newChannel.alert_light = 'Off'
    newChannel.volume_offset = '0'
    newChannel.p_ch = 'Off'
    newChannel.number_tag = null
    newChannel.priority = false
    
    // Close dialog
    showAddChannelDialog.value = false
    
    // Reload the favorites list to show the new channel
    await loadFavoritesList()
    
  } catch (error) {
    console.error('Error adding channel:', error)
    const errorMsg = error.response?.data?.detail || error.message || 'Failed to add channel'
    $q.notify({ type: 'negative', message: errorMsg })
  }
}

const addDepartmentToFavorites = async () => {
  // Validate department name
  if (!newDepartment.value.name_tag || newDepartment.value.name_tag.trim() === '') {
    $q.notify({ type: 'negative', message: 'Department name is required' })
    return
  }

  // Validate name length (max 255 characters)
  if (newDepartment.value.name_tag.length > 255) {
    $q.notify({ type: 'negative', message: 'Department name must be 255 characters or less' })
    return
  }

  try {
    // Get the selected favorites list
    if (!selectedFavoritesNode.value || selectedFavoritesNode.value.type !== 'favorites_list') {
      $q.notify({ type: 'negative', message: 'Please select a favorites list to add department to' })
      return
    }

    const favoritesList = selectedFavoritesNode.value.favData
    if (!favoritesList || !favoritesList.id) {
      $q.notify({ type: 'negative', message: 'Invalid favorites list selected' })
      return
    }

    // Create payload for API - use favorites_list FK now
    const payload = {
      name_tag: newDepartment.value.name_tag,
      location_type: newDepartment.value.location_type || 'Conventional',
      latitude: newDepartment.value.latitude || null,
      longitude: newDepartment.value.longitude || null,
      range_miles: newDepartment.value.range_miles || null,
      enabled: newDepartment.value.enabled ? true : false,
      cgroup_id: `CG_${Date.now()}`, // Generate a unique ID
      favorites_list: favoritesList.id // Link directly to FavoritesList
    }

    // POST to API to create new channel group (department)
    const response = await api.post('/usersettings/channel-groups/', payload)
    
    $q.notify({ type: 'positive', message: `Department "${newDepartment.value.name_tag}" added successfully!` })
    
    // Reset form
    newDepartment.value.name_tag = ''
    newDepartment.value.location_type = 'Conventional'
    newDepartment.value.latitude = null
    newDepartment.value.longitude = null
    newDepartment.value.range_miles = null
    newDepartment.value.enabled = true
    
    // Close dialog
    showAddDepartmentDialog.value = false
    
    // Reload the favorites list to show the new department
    await loadFavoritesList()
    
  } catch (error) {
    console.error('Error adding department:', error)
    const errorMsg = error.response?.data?.detail || error.message || 'Failed to add department'
    $q.notify({ type: 'negative', message: errorMsg })
  }
}

const editFavoritesList = (favoritesList) => {
  editingFavorites.value = {
    id: favoritesList.id,
    user_name: favoritesList.user_name
  }
  showEditFavoritesDialog.value = true
}

const updateFavoritesList = async () => {
  if (!editingFavorites.value.user_name || editingFavorites.value.user_name.trim() === '') {
    $q.notify({ type: 'negative', message: 'Favorites list name is required' })
    return
  }

  try {
    await api.patch(`/usersettings/favorites-lists/${editingFavorites.value.id}/`, {
      user_name: editingFavorites.value.user_name
    })
    
    $q.notify({ type: 'positive', message: 'Favorites list name updated successfully!' })
    showEditFavoritesDialog.value = false
    await loadFavoritesList()
  } catch (error) {
    console.error('Error updating favorites list:', error)
    $q.notify({ type: 'negative', message: 'Failed to update favorites list name' })
  }
}

const editDepartment = (department) => {
  editingDepartment.value = {
    id: department.id,
    name_tag: department.name_tag
  }
  showEditDepartmentDialog.value = true
}

const updateDepartment = async () => {
  if (!editingDepartment.value.name_tag || editingDepartment.value.name_tag.trim() === '') {
    $q.notify({ type: 'negative', message: 'Department name is required' })
    return
  }

  try {
    await api.patch(`/usersettings/channel-groups/${editingDepartment.value.id}/`, {
      name_tag: editingDepartment.value.name_tag
    })
    
    $q.notify({ type: 'positive', message: 'Department name updated successfully!' })
    showEditDepartmentDialog.value = false
    await loadFavoritesList()
  } catch (error) {
    console.error('Error updating department:', error)
    $q.notify({ type: 'negative', message: 'Failed to update department name' })
  }
}

const editChannel = (channel) => {
  editingChannel.value = {
    id: channel.id,
    name_tag: channel.name_tag
  }
  showEditChannelDialog.value = true
}

const updateChannel = async () => {
  if (!editingChannel.value.name_tag || editingChannel.value.name_tag.trim() === '') {
    $q.notify({ type: 'negative', message: 'Channel name is required' })
    return
  }

  try {
    await api.patch(`/usersettings/frequencies/${editingChannel.value.id}/`, {
      name_tag: editingChannel.value.name_tag
    })
    
    $q.notify({ type: 'positive', message: 'Channel name updated successfully!' })
    showEditChannelDialog.value = false
    await loadFavoritesList()
  } catch (error) {
    console.error('Error updating channel:', error)
    $q.notify({ type: 'negative', message: 'Failed to update channel name' })
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

/* Rotating animation for processing icon */
@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.rotating {
  animation: rotate 2s linear infinite;
}
</style>
