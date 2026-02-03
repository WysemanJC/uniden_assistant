<template>
  <q-layout view="hHh Lpr fFf">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-toolbar-title>Uniden Assistant</q-toolbar-title>
      </q-toolbar>
    </q-header>



    <q-page-container>
      <q-page class="q-pa-md">
        
        <!-- Favourites Editor Section -->
        <div v-if="activeSection === 'favorites'">
          <!-- Tree + Table Layout for Favorites -->
          <div class="row q-col-gutter-md">
            <!-- Left Pane: Favorites Lists Tree -->
            <div class="col-12 col-md-3">
              <q-card flat bordered style="height: 85vh; overflow-y: auto;">
                <q-card-section class="q-pa-sm">
                  <div class="row justify-end q-mb-md q-gutter-sm">
                    <q-btn
                      color="primary"
                      label="Load Favourites"
                      icon="cloud_upload"
                      size="sm"
                      @click="loadFavourites"
                    />
                    <q-btn
                      color="secondary"
                      label="Download Favourites"
                      icon="cloud_download"
                      size="sm"
                      @click="exportFavoritesFolder"
                    />
                  </div>
                  <q-tree
                    :nodes="favoritesTreeNodes"
                    node-key="id"
                    v-model:selected="selectedFavoritesNodeId"
                    v-model:expanded="expandedFavoritesNodes"
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
              <q-card flat bordered style="height: 85vh; overflow-y: auto;">
                <q-card-section class="q-pa-sm">
                  <!-- Favorites Root Node - Favorite Lists Table -->
                  <div v-if="selectedFavoritesNode && selectedFavoritesNode.type === 'root'">
                    <div class="text-h6 q-mb-md">Favourite Lists</div>

                    <div class="row q-gutter-sm q-mb-md items-center">
                      <div class="row q-gutter-sm">
                        <q-btn
                          color="primary"
                          label="Export Selected"
                          icon="download"
                          :disable="selectedFavoritesListIds.length === 0"
                          @click="exportSelectedFavoritesLists"
                        />
                        <q-btn
                          color="secondary"
                          label="Import JSON"
                          icon="upload"
                          @click="importFavoritesJSON"
                        />
                      </div>
                      <q-space />
                      <div class="row q-gutter-sm">
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
                          :disable="selectedFavoritesListIds.length === 0"
                          @click="deleteSelectedFavoritesLists"
                        />
                      </div>
                    </div>

                    <q-table
                      flat
                      bordered
                      :rows="favorites"
                      :columns="[
                        { name: 'checkbox', label: '', field: '', align: 'left', style: 'width: 50px' },
                        { name: 'user_name', label: 'Favourite List Name', field: 'user_name', align: 'left' },
                        { name: 'filename', label: 'Filename', field: 'filename', align: 'left' },
                        { name: 'location_control', label: 'Location Control', field: 'location_control', align: 'left', style: 'width: 120px' },
                        { name: 'monitor', label: 'Monitor', field: 'monitor', align: 'left', style: 'width: 100px' },
                        { name: 'quick_key', label: 'Quick Key', field: 'quick_key', align: 'left', style: 'width: 100px' },
                        { name: 'number_tag', label: 'Number Tag', field: 'number_tag', align: 'left', style: 'width: 100px' },
                        { name: 'actions', label: 'Actions', field: 'actions', align: 'center', style: 'width: 120px' }
                      ]"
                      row-key="id"
                      :pagination="{ rowsPerPage: 0 }"
                      hide-pagination
                      style="height: 100%"
                    >
                      <template v-slot:header-cell-checkbox="props">
                        <q-th :props="props">
                          <q-checkbox
                            :model-value="selectedFavoritesListIds.length === favorites.length && favorites.length > 0"
                            :indeterminate="selectedFavoritesListIds.length > 0 && selectedFavoritesListIds.length < favorites.length"
                            @update:model-value="toggleAllFavoritesLists"
                          />
                        </q-th>
                      </template>
                      <template v-slot:body-cell-checkbox="props">
                        <q-td :props="props">
                          <q-checkbox
                            :model-value="selectedFavoritesListIds.includes(props.row.id)"
                            @update:model-value="toggleFavoritesListSelection(props.row.id)"
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
                            @click="editFavoritesList(props.row)"
                          >
                            <q-tooltip>Edit Favorites List</q-tooltip>
                          </q-btn>
                          <q-btn
                            flat
                            round
                            dense
                            icon="delete"
                            color="negative"
                            size="sm"
                            class="q-ml-xs"
                            @click="deleteSingleFavoritesList(props.row)"
                          >
                            <q-tooltip>Delete Favorites List</q-tooltip>
                          </q-btn>
                        </q-td>
                      </template>
                    </q-table>
                  </div>

                  <!-- Department/Channel Details View -->
                  <div v-else-if="selectedFavoritesNode && selectedFavoritesNode.type === 'department'">
                    <div class="row items-center q-mb-md">
                      <div class="col">
                        <div class="text-h6">{{ selectedFavoritesNode.label }}</div>
                        <div class="text-caption text-grey-7">{{ selectedFavoritesList?.user_name || 'Favorites List' }}</div>
                      </div>
                      <q-btn
                        color="secondary"
                        label="Add Channel"
                        icon="add"
                        size="sm"
                        @click="openAddChannelDialog"
                      />
                    </div>

                    <div v-if="favoritesChannels.length > 0" style="height: calc(100vh - 380px); overflow-y: auto;">
                      <q-table
                        :rows="favoritesChannels"
                        :columns="favoritesChannelColumnsBySystem"
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
                            <q-btn
                              flat
                              round
                              dense
                              icon="delete"
                              color="negative"
                              size="sm"
                              class="q-ml-xs"
                              @click="deleteChannel(props.row)"
                            >
                              <q-tooltip>Delete Channel</q-tooltip>
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

                  <!-- Systems List View (when Favorites List selected) -->
                  <div v-else-if="selectedFavoritesNode && selectedFavoritesNode.type === 'favorites_list'">
                    <div class="row items-center q-mb-md">
                      <div class="col">
                        <div class="text-h6">{{ selectedFavoritesNode.label }}</div>
                        <div class="text-caption text-grey-7">Systems</div>
                      </div>
                      <q-btn
                        color="secondary"
                        label="Add System"
                        icon="add"
                        size="sm"
                        @click="openAddSystemDialog"
                      />
                    </div>

                    <!-- Systems table -->
                    <div v-if="systemsData && systemsData.length > 0" style="height: calc(100vh - 380px); overflow-y: auto;">
                      <q-table
                        :rows="systemsData"
                        :columns="systemsColumns"
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
                              @click="editSystem(props.row)"
                            >
                              <q-tooltip>Edit System</q-tooltip>
                            </q-btn>
                            <q-btn
                              flat
                              round
                              dense
                              icon="delete"
                              color="negative"
                              size="sm"
                              class="q-ml-xs"
                              @click="deleteSystem(props.row)"
                            >
                              <q-tooltip>Delete System</q-tooltip>
                            </q-btn>
                          </q-td>
                        </template>
                      </q-table>
                    </div>

                    <div v-else class="text-center q-pa-xl text-grey-7">
                      <q-icon name="info" size="2em" />
                      <div class="q-mt-md text-caption">No systems found</div>
                    </div>
                  </div>

                  <!-- Departments List View (when System selected) -->
                  <div v-else-if="selectedFavoritesNode && selectedFavoritesNode.type === 'system'">
                    <div class="row items-center q-mb-md">
                      <div class="col">
                        <div class="text-h6">{{ selectedFavoritesNode.label }}</div>
                        <div class="text-caption text-grey-7">Departments</div>
                      </div>
                      <q-btn
                        color="secondary"
                        label="Add Department"
                        icon="add"
                        size="sm"
                        @click="openAddDepartmentDialog"
                      />
                    </div>

                    <!-- Departments table -->
                    <div v-if="departmentsData && departmentsData.length > 0" style="height: calc(100vh - 380px); overflow-y: auto;">
                      <q-table
                        :rows="departmentsData"
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
                            <q-btn
                              flat
                              round
                              dense
                              icon="delete"
                              color="negative"
                              size="sm"
                              class="q-ml-xs"
                              @click="deleteDepartment(props.row)"
                            >
                              <q-tooltip>Delete Department</q-tooltip>
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
          <div class="text-h6">{{ isEditMode ? 'Edit Channel' : 'Add Channel' }}</div>
          <q-space />
          <q-btn icon="close" flat round dense @click="showAddChannelDialog = false" />
        </q-card-section>

        <q-card-section class="q-pt-none" style="max-height: 600px; overflow-y: auto;">
          <template v-if="isTrunkSystemType(selectedFavoritesNode?.system_type || newChannel.system_type)">
            <!-- Trunk System Fields -->
            <div class="text-subtitle2 q-mb-md">Channel Details</div>
            <q-input
              v-model="newChannel.name_tag"
              label="Channel Name (NameTag)"
              hint="Max 64 characters"
              maxlength="64"
              counter
              class="q-mb-md"
            />
            <q-select
              v-model="newChannel.avoid"
              :options="['Off', 'On']"
              label="Avoid"
              class="q-mb-md"
            />
            <q-input
              v-model="newChannel.frequency"
              label="TGID"
              hint="Talkgroup ID"
              class="q-mb-md"
            />
            <q-select
              v-model="newChannel.tdma_slot"
              :options="['Any', '1', '2']"
              label="TDMA Slot"
              class="q-mb-md"
            />
            <q-select
              v-model="newChannel.func_tag_id"
              :options="serviceTypes"
              option-value="value"
              option-label="label"
              emit-value
              map-options
              label="Service Type (FuncTagId)"
              class="q-mb-md"
            />
            <q-select
              v-model.number="newChannel.delay"
              :options="[30, 10, 5, 4, 3, 2, 1, 0, -5, -10]"
              label="Delay (seconds)"
              class="q-mb-md"
            />
            <q-select
              v-model="newChannel.alert_tone"
              :options="['Off', '1', '2', '3', '4', '5', '6', '7', '8', '9']"
              label="Alert Tone"
              class="q-mb-md"
            />
            <q-select
              v-model="newChannel.alert_color"
              :options="['Off', 'Blue', 'Red', 'Magenta', 'Green', 'Cyan', 'Yellow', 'White']"
              label="Alert Light Color"
              class="q-mb-md"
            />
            <q-select
              v-model="newChannel.alert_pattern"
              :options="['On', 'Slow Blink', 'Fast Blink']"
              label="Alert Light Pattern"
              class="q-mb-md"
            />
            <q-select
              v-model.number="newChannel.volume_offset"
              :options="['-3', '-2', '-1', '0', '1', '2', '3']"
              label="Volume Offset (dB)"
              class="q-mb-md"
            />
            <q-input
              v-model.number="newChannel.number_tag"
              label="Number Tag"
              type="number"
              hint="Off or 0-999"
              class="q-mb-md"
            />
            <q-select
              v-model="newChannel.p_ch"
              :options="['Off', 'On']"
              label="P-Ch"
              class="q-mb-md"
            />
          </template>

          <template v-else>
            <!-- Conventional Fields -->
            <div class="text-subtitle2 q-mb-md">Basic Information</div>
            <q-input
              v-model="newChannel.name_tag"
              label="Channel Name (NameTag)"
              hint="Max 64 characters"
              maxlength="64"
              counter
              class="q-mb-md"
            />
            <q-select
              v-model="newChannel.avoid"
              :options="['Off', 'On']"
              label="Avoid"
              class="q-mb-md"
            />
            <q-input
              v-model.number="newChannel.frequency"
              label="Frequency (MHz)"
              type="number"
              hint="Enter frequency in MHz (will be stored as Hz)"
              class="q-mb-md"
            />
            <q-select
              v-model="newChannel.modulation"
              :options="['FM', 'NFM', 'AM', 'AUTO']"
              label="Modulation"
              class="q-mb-md"
            />

            <div class="text-subtitle2 q-mb-md q-mt-lg">Sub-Audio Options</div>
            <q-input
              v-model="newChannel.audio_option"
              label="Audio Option"
              hint="e.g., TONE=67.0, NAC=293, ColorCode=1, RAN=12, Area=2"
              class="q-mb-md"
            />

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

            <div class="text-subtitle2 q-mb-md q-mt-lg">Service Type</div>
            <q-select
              v-model="newChannel.func_tag_id"
              :options="serviceTypes"
              option-value="value"
              option-label="label"
              emit-value
              map-options
              label="Service Type (FuncTagId)"
              hint="Function/service type for this channel"
              class="q-mb-md"
            />

            <div class="text-subtitle2 q-mb-md q-mt-lg">Alert Settings</div>
            <q-select
              v-model="newChannel.alert_tone"
              :options="['Off', '1', '2', '3', '4', '5', '6', '7', '8', '9']"
              label="Alert Tone"
              class="q-mb-md"
            />
            <q-select
              v-model="newChannel.alert_color"
              :options="['Off', 'Blue', 'Red', 'Magenta', 'Green', 'Cyan', 'Yellow', 'White']"
              label="Alert Light Color"
              class="q-mb-md"
            />
            <q-select
              v-model="newChannel.alert_pattern"
              :options="['On', 'Slow Blink', 'Fast Blink']"
              label="Alert Light Pattern"
              class="q-mb-md"
            />

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
          </template>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancel" @click="showAddChannelDialog = false" />
          <q-btn
            flat
            :label="isEditMode ? 'Save' : 'Add Channel'"
            color="primary"
            @click="isEditMode ? updateChannel() : addChannelToFavorites()"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Create/Edit Favorites List Dialog -->
    <q-dialog v-model="showCreateFavoritesListDialog">
      <q-card style="min-width: 700px; max-width: 900px">
        <q-card-section class="row items-center q-pb-none">
          <div class="text-h6">{{ isEditFavoritesListMode ? 'Edit Favorites List' : 'Create New Favorites List' }}</div>
          <q-space />
          <q-btn icon="close" flat round dense @click="showCreateFavoritesListDialog = false" />
        </q-card-section>

        <q-card-section style="max-height: 70vh; overflow-y: auto;">
          <q-input
            v-model="newFavoritesList.user_name"
            label="Favorite List Name"
            hint="Display name for this favorites list"
            class="q-mb-md"
            outlined
            dense
          />
          <div class="row q-gutter-md q-mb-md">
            <div class="col">
              <q-select
                v-model="newFavoritesList.location_control"
                :options="['On', 'Off']"
                label="Location Control"
                outlined
                dense
                emit-value
                map-options
              />
            </div>
            <div class="col">
              <q-select
                v-model="newFavoritesList.monitor"
                :options="['On', 'Off']"
                label="Monitor"
                outlined
                dense
                emit-value
                map-options
              />
            </div>
          </div>
          <div class="row q-gutter-md">
            <div class="col">
              <q-input
                v-model="newFavoritesList.quick_key"
                label="Quick Key"
                hint="Off or 0-99"
                outlined
                dense
                class="q-mb-md"
              />
            </div>
            <div class="col">
              <q-input
                v-model="newFavoritesList.number_tag"
                label="Number Tag"
                hint="Off or 0-99"
                outlined
                dense
                class="q-mb-md"
              />
            </div>
          </div>

          <!-- Startup Keys Section -->
          <q-separator class="q-my-md" />
          <div class="row items-center q-mb-sm">
            <div class="text-subtitle2">Startup Keys Status</div>
            <q-space />
            <q-btn flat dense size="sm" label="Select All" @click="selectAllStartupKeys(true)" />
            <q-btn flat dense size="sm" label="Clear All" @click="selectAllStartupKeys(false)" />
          </div>
          <div class="row q-gutter-sm q-mb-md">
            <div v-for="i in 10" :key="i" class="col-auto">
              <q-checkbox
                :model-value="newFavoritesList.startup_keys[i - 1] === 'On'"
                @update:model-value="newFavoritesList.startup_keys[i - 1] = $event ? 'On' : 'Off'"
                :label="String(i - 1)"
                dense
                style="min-width: 60px;"
              />
            </div>
          </div>

          <!-- System Quick Keys Section -->
          <q-separator class="q-my-md" />
          <div class="row items-center q-mb-sm">
            <div class="text-subtitle2">System Quick Keys Status (S-Qkey)</div>
            <q-space />
            <q-btn flat dense size="sm" label="Select All" @click="selectAllSQkeys(true)" />
            <q-btn flat dense size="sm" label="Clear All" @click="selectAllSQkeys(false)" />
          </div>
          <div class="row q-gutter-sm" style="max-height: 300px; overflow-y: auto;">
            <div v-for="i in 100" :key="i" class="col-auto">
              <q-checkbox
                :model-value="newFavoritesList.s_qkeys[i - 1] === 'On'"
                @update:model-value="newFavoritesList.s_qkeys[i - 1] = $event ? 'On' : 'Off'"
                :label="String(i - 1).padStart(2, '0')"
                dense
                style="min-width: 70px;"
              />
            </div>
          </div>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancel" @click="showCreateFavoritesListDialog = false" />
          <q-btn
            flat
            :label="isEditFavoritesListMode ? 'Save' : 'Create'"
            color="primary"
            @click="isEditFavoritesListMode ? updateFavoritesList() : submitCreateFavoritesList()"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Add/Edit System Dialog -->
    <q-dialog v-model="showSystemDialog">
      <q-card style="min-width: 560px; max-width: 680px">
        <q-card-section class="row items-center q-pb-none">
          <div class="text-h6">{{ isEditSystemMode ? 'Edit System' : 'Add System' }}</div>
          <q-space />
          <q-btn icon="close" flat round dense @click="showSystemDialog = false" />
        </q-card-section>

        <q-card-section class="q-pt-none" style="max-height: 600px; overflow-y: auto;">
          <div class="text-subtitle2 q-mb-md">System Details</div>
          <q-input
            v-model="newSystem.system_name"
            label="System Name"
            maxlength="64"
            counter
            class="q-mb-md"
          />
          <q-select
            v-model="newSystem.avoid"
            :options="['Off', 'On']"
            label="Avoid"
            class="q-mb-md"
          />
          <q-select
            v-model="newSystem.system_type"
            :options="systemTypeOptions"
            label="System Type"
            class="q-mb-md"
          />
          <q-input
            v-model="newSystem.quick_key"
            label="Quick Key"
            hint="Off or 0-99"
            class="q-mb-md"
          />
          <q-input
            v-model="newSystem.number_tag"
            label="Number Tag"
            hint="Off or 0-999"
            class="q-mb-md"
          />
          <q-input
            v-model.number="newSystem.hold_time"
            label="Hold Time"
            type="number"
            hint="0-255 seconds"
            class="q-mb-md"
          />
          <q-select
            v-model="newSystem.analog_agc"
            :options="['Off', 'On']"
            label="Analog AGC"
            class="q-mb-md"
          />
          <q-select
            v-model="newSystem.digital_agc"
            :options="['Off', 'On']"
            label="Digital AGC"
            class="q-mb-md"
          />
          <template v-if="!isTrunkSystemType(newSystem.system_type)">
            <q-input
              v-model.number="newSystem.digital_waiting_time"
              label="Digital Waiting Time"
              type="number"
              hint="0-1000 ms"
              class="q-mb-md"
            />
            <q-select
              v-model="newSystem.digital_threshold_mode"
              :options="['Manual', 'Auto', 'Default']"
              label="Digital Threshold Mode"
              class="q-mb-md"
            />
            <q-input
              v-model.number="newSystem.digital_threshold_level"
              label="Digital Threshold Level"
              type="number"
              hint="5-13"
              class="q-mb-md"
            />
          </template>

          <template v-if="isTrunkSystemType(newSystem.system_type)">
            <q-select
              v-model="newSystem.id_search"
              :options="['Off', 'On']"
              label="ID: Search"
              class="q-mb-md"
            />
            <q-select
              v-model="newSystem.emergency_alert"
              :options="['Off', '1', '2', '3', '4', '5', '6', '7', '8', '9']"
              label="Emergency Alert"
              class="q-mb-md"
            />
            <q-select
              v-model="newSystem.emergency_alert_light"
              :options="['Off', 'On']"
              label="Emergency Alert Light"
              class="q-mb-md"
            />
            <q-select
              v-model="newSystem.status_bit"
              :options="['Ignore', 'Yes']"
              label="Status Bit"
              class="q-mb-md"
            />
            <q-input
              v-model="newSystem.p25_nac"
              label="P25 NAC"
              hint="Srch or 0-FFF"
              class="q-mb-md"
            />
            <q-select
              v-model="newSystem.priority_id_scan"
              :options="['Off', 'On']"
              label="Priority ID Scan"
              class="q-mb-md"
            />
            <q-select
              v-model="newSystem.end_code"
              :options="['Analog', 'Analog+Digital', 'Ignore']"
              label="End Code"
              class="q-mb-md"
            />
            <q-input
              v-model="newSystem.nxdn_format"
              label="NXDN TGID Format"
              class="q-mb-md"
            />
          </template>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancel" @click="showSystemDialog = false" />
          <q-btn
            flat
            :label="isEditSystemMode ? 'Save' : 'Add System'"
            color="primary"
            @click="isEditSystemMode ? updateSystem() : addSystemToFavorites()"
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

    <!-- Add/Edit Department Dialog -->
    <q-dialog v-model="showDepartmentDialog">
      <q-card style="min-width: 520px; max-width: 640px">
        <q-card-section class="row items-center q-pb-none">
          <div class="text-h6">{{ isEditDepartmentMode ? 'Edit Department' : 'Add Department' }}</div>
          <q-space />
          <q-btn icon="close" flat round dense @click="showDepartmentDialog = false" />
        </q-card-section>

        <q-card-section class="q-pt-none" style="max-height: 600px; overflow-y: auto;">
          <div class="text-subtitle2 q-mb-md">Department Details</div>
          <q-input
            v-model="newDepartment.name_tag"
            label="Department Name (NameTag)"
            maxlength="255"
            counter
            class="q-mb-md"
          />
          <q-select
            v-model="newDepartment.avoid"
            :options="['Off', 'On']"
            label="Avoid"
            class="q-mb-md"
          />
          <q-select
            v-model="newDepartment.location_type"
            :options="['Circle', 'Rectangles']"
            label="Location Type"
            class="q-mb-md"
          />
          <q-input
            v-model.number="newDepartment.latitude"
            label="Latitude"
            type="number"
            step="0.00001"
            class="q-mb-md"
          />
          <q-input
            v-model.number="newDepartment.longitude"
            label="Longitude"
            type="number"
            step="0.00001"
            class="q-mb-md"
          />
          <q-input
            v-model.number="newDepartment.range_miles"
            label="Range (miles)"
            type="number"
            class="q-mb-md"
          />
          <q-input
            v-model="newDepartment.quick_key"
            label="Quick Key"
            hint="Off or 0-99"
            class="q-mb-md"
          />
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancel" @click="showDepartmentDialog = false" />
          <q-btn
            flat
            :label="isEditDepartmentMode ? 'Save' : 'Add Department'"
            color="primary"
            @click="isEditDepartmentMode ? updateDepartment() : addDepartmentToSystem()"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Edit Channel Dialog -->


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
import { ref, onMounted, computed, onBeforeUnmount, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useScannerStore } from '../stores/scanner'
import api, { sdAPI } from '../api'
import { useQuasar, QSeparator, QCheckbox, QTable } from 'quasar'
import ChannelGroupMapDialog from '../components/ChannelGroupMapDialog.vue'

const route = useRoute()
const router = useRouter()
const scanner = useScannerStore()
const $q = useQuasar()

// Navigation
const activeSection = ref('favorites')

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
const expandedFavoritesNodes = ref(['favorites_root'])
const systemsData = ref([])
const systemsLoading = ref(false)
const departmentsData = ref([])
const departmentsLoading = ref(false)
const selectedFavoritesListIds = ref([])  // For multi-export
const favoritesColumns = [
  { name: 'user_name', label: 'User Name', field: 'user_name', align: 'left', sortable: true },
  { name: 'filename', label: 'Filename', field: 'filename', align: 'left', sortable: true },
  { name: 'location_control', label: 'Location Control', field: 'location_control', align: 'center', sortable: true },
  { name: 'monitor', label: 'Monitor', field: 'monitor', align: 'center', sortable: true },
  { name: 'quick_key', label: 'Quick Key', field: 'quick_key', align: 'center', sortable: true },
  { name: 'number_tag', label: 'Number Tag', field: 'number_tag', align: 'center', sortable: true },
  { name: 'startup_keys', label: 'Startup Keys', field: row => {
    if (!row.startup_keys || !Array.isArray(row.startup_keys)) return 'None';
    // Handle both boolean and string values
    const onKeys = row.startup_keys.map((val, idx) => {
      return (val === true || val === 'On') ? idx : null;
    }).filter(x => x !== null);
    return onKeys.length > 0 ? onKeys.join(', ') : 'None';
  }, align: 'center' }
]

const favoritesChannelColumnsConventional = [
  { name: 'name_tag', label: 'Channel Name', field: 'name_tag', align: 'left', sortable: true },
  { name: 'avoid', label: 'Avoid', field: 'avoid', align: 'center', sortable: true },
  { name: 'frequency', label: 'Frequency', field: 'frequency', align: 'left', sortable: true },
  { name: 'modulation', label: 'Modulation', field: 'modulation', align: 'left', sortable: true },
  { name: 'audio_option', label: 'Audio Option', field: 'audio_option', align: 'left', sortable: true },
  { name: 'func_tag_id', label: 'Service Type', field: 'func_tag_id', align: 'center', sortable: true },
  { name: 'attenuator', label: 'Attenuator', field: 'attenuator', align: 'center', sortable: true },
  { name: 'delay', label: 'Delay', field: 'delay', align: 'center', sortable: true },
  { name: 'alert_tone', label: 'Alert Tone', field: 'alert_tone', align: 'center', sortable: true },
  { name: 'alert_color', label: 'Alert Color', field: 'alert_color', align: 'center', sortable: true },
  { name: 'alert_pattern', label: 'Alert Pattern', field: 'alert_pattern', align: 'center', sortable: true },
  { name: 'volume_offset', label: 'Volume Offset', field: 'volume_offset', align: 'center', sortable: true },
  { name: 'number_tag', label: 'Number Tag', field: 'number_tag', align: 'center', sortable: true },
  { name: 'p_ch', label: 'P-Ch', field: row => row.p_ch || row.priority_channel || 'Off', align: 'center', sortable: true },
  { name: 'actions', label: 'Actions', field: 'actions', align: 'center' }
]

const favoritesChannelColumnsTrunk = [
  { name: 'name_tag', label: 'Channel Name', field: 'name_tag', align: 'left', sortable: true },
  { name: 'avoid', label: 'Avoid', field: 'avoid', align: 'center', sortable: true },
  { name: 'frequency', label: 'TGID', field: row => row.tgid ?? row.frequency, align: 'left', sortable: true },
  { name: 'tdma_slot', label: 'TDMA Slot', field: row => row.tdma_slot || 'Any', align: 'center', sortable: true },
  { name: 'func_tag_id', label: 'Service Type', field: 'func_tag_id', align: 'center', sortable: true },
  { name: 'delay', label: 'Delay', field: 'delay', align: 'center', sortable: true },
  { name: 'alert_tone', label: 'Alert Tone', field: 'alert_tone', align: 'center', sortable: true },
  { name: 'alert_color', label: 'Alert Color', field: 'alert_color', align: 'center', sortable: true },
  { name: 'alert_pattern', label: 'Alert Pattern', field: 'alert_pattern', align: 'center', sortable: true },
  { name: 'volume_offset', label: 'Volume Offset', field: 'volume_offset', align: 'center', sortable: true },
  { name: 'number_tag', label: 'Number Tag', field: 'number_tag', align: 'center', sortable: true },
  { name: 'p_ch', label: 'P-Ch', field: row => row.p_ch || row.priority_channel || 'Off', align: 'center', sortable: true },
  { name: 'actions', label: 'Actions', field: 'actions', align: 'center' }
]

const favoritesListDepartmentColumns = [
  { name: 'name_tag', label: 'Department Name', field: 'name_tag', align: 'left', sortable: true },
  { name: 'avoid', label: 'Avoid', field: 'avoid', align: 'center', sortable: true },
  { name: 'system_type', label: 'Type', field: 'system_type', align: 'center', sortable: true },
  { name: 'location_type', label: 'Location Type', field: 'location_type', align: 'left', sortable: true },
  { name: 'quick_key', label: 'Quick Key', field: 'quick_key', align: 'center', sortable: true },
  { name: 'actions', label: 'Actions', field: 'actions', align: 'center' }
]

const systemsColumns = [
  { name: 'system_name', label: 'System Name', field: 'system_name', align: 'left', sortable: true },
  { name: 'avoid', label: 'Avoid', field: 'avoid', align: 'center', sortable: true },
  { name: 'system_type', label: 'System Type', field: 'system_type', align: 'center', sortable: true },
  { name: 'id_search', label: 'ID: Search', field: 'id_search', align: 'center', sortable: true },
  { name: 'emergency_alert', label: 'Emergency Alert', field: 'emergency_alert', align: 'center', sortable: true },
  { name: 'emergency_alert_light', label: 'Emergency Alert Light', field: 'emergency_alert_light', align: 'center', sortable: true },
  { name: 'status_bit', label: 'Status Bit', field: 'status_bit', align: 'center', sortable: true },
  { name: 'p25_nac', label: 'P25 NAC', field: 'p25_nac', align: 'center', sortable: true },
  { name: 'quick_key', label: 'Quick Key', field: 'quick_key', align: 'center', sortable: true },
  { name: 'number_tag', label: 'Number Tag', field: 'number_tag', align: 'center', sortable: true },
  { name: 'hold_time', label: 'Hold Time', field: 'hold_time', align: 'center', sortable: true },
  { name: 'priority_id_scan', label: 'Priority ID Scan', field: 'priority_id_scan', align: 'center', sortable: true },
  { name: 'end_code', label: 'End Code', field: 'end_code', align: 'center', sortable: true },
  { name: 'nxdn_format', label: 'NXDN TGID Format', field: 'nxdn_format', align: 'center', sortable: true },
  { name: 'analog_agc', label: 'Analog AGC', field: 'analog_agc', align: 'center', sortable: true },
  { name: 'digital_agc', label: 'Digital AGC', field: 'digital_agc', align: 'center', sortable: true },
  { name: 'digital_waiting_time', label: 'Digital Waiting Time', field: 'digital_waiting_time', align: 'center', sortable: true },
  { name: 'digital_threshold_mode', label: 'Digital Threshold Mode', field: 'digital_threshold_mode', align: 'center', sortable: true },
  { name: 'digital_threshold_level', label: 'Digital Threshold Level', field: 'digital_threshold_level', align: 'center', sortable: true },
  { name: 'actions', label: 'Actions', field: 'actions', align: 'center' }
]

const isTrunkSystemType = (systemType) => {
  if (!systemType) return false
  return systemType !== 'Conventional'
}

const favoritesChannelColumnsBySystem = computed(() => {
  if (isTrunkSystemType(selectedFavoritesNode.value?.system_type)) {
    return favoritesChannelColumnsTrunk
  }
  return favoritesChannelColumnsConventional
})

const favoritesTreeNodes = computed(() => {
  console.log('[favoritesTreeNodes] Computing tree nodes, favorites.value:', favorites.value)
  
  const favoritesList = favorites.value.map((fav, idx) => {
    console.log(`[favoritesTreeNodes] Processing favorite #${idx}: ${fav.user_name}`)
    
    // Group departments by their system
    const systemsMap = new Map()
    
    if (fav.groups && fav.groups.length > 0) {
      fav.groups
        .filter(group => !group.is_system_placeholder)  // Filter out placeholder departments
        .forEach((group, gIdx) => {
          const systemName = group.system_name || 'Unknown System'
          const systemType = group.system_type || 'Conventional'
          const systemKey = `${systemType}_${systemName}`
          
          if (!systemsMap.has(systemKey)) {
            systemsMap.set(systemKey, {
              system_name: systemName,
              system_type: systemType,
              departments: []
            })
          }
          
          systemsMap.get(systemKey).departments.push({
            id: `dept_${fav.id}_${gIdx}`,
            label: `${group.name_tag || `Department ${gIdx + 1}`} (${group.freq_count || 0})`,
            type: 'department',
            system_type: group.system_type,
            favId: fav.id,
            groupId: group.id,
            channel_count: group.freq_count,
            groupData: group
          })
        })
    }
    
    // Convert systems map to tree nodes
    const systemsChildren = Array.from(systemsMap.values()).map((system, sIdx) => {
      const matched = systemsData.value?.find(sys =>
        sys.system_name === system.system_name && sys.system_type === system.system_type
      )

      return ({
      id: `sys_${fav.id}_${sIdx}`,
      label: `${system.system_name} (${system.system_type})`,
      type: 'system',
      system_type: system.system_type,
      system_name: system.system_name,
      systemId: matched?.id || null,
      favId: fav.id,
      favData: fav,
      children: system.departments
      })
    })
    
    return {
      id: `fav_${fav.id}`,
      label: `${fav.user_name} (${fav.filename})`,
      type: 'favorites_list',
      favData: fav,
      children: systemsChildren
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
const showCreateFavoritesListDialog = ref(false)
const isEditFavoritesListMode = ref(false)
const newFavoritesList = ref({
  user_name: '',
  location_control: 'Off',
  monitor: 'On',
  quick_key: 'Off',
  number_tag: 'Off',
  s_qkeys: Array(100).fill('Off'),
  startup_keys: Array(10).fill('Off')
})
const isEditMode = ref(false)
const newChannel = ref({
  name_tag: '',
  description: '',
  frequency: '',
  modulation: 'AUTO',
  audio_option: '',
  func_tag_id: 21,  // 21 = Other (default)
  avoid: 'Off',
  enabled: true,
  delay: 15,
  attenuator: 'Off',
  alert_tone: 'Off',
  alert_light: 'Off',
  alert_color: 'Off',
  alert_pattern: 'On',
  volume_offset: '0',
  p_ch: 'Off',
  number_tag: null,
  priority: 0,
  tdma_slot: 'Any',
  system_type: 'Conventional'
})

// Service types for func_tag_id dropdown (from specification)
const serviceTypes = [
  { label: '1 - Multi-Dispatch', value: 1 },
  { label: '2 - Law Dispatch', value: 2 },
  { label: '3 - Fire Dispatch', value: 3 },
  { label: '4 - EMS Dispatch', value: 4 },
  { label: '6 - Multi-Tac', value: 6 },
  { label: '7 - Law Tac', value: 7 },
  { label: '8 - Fire-Tac', value: 8 },
  { label: '9 - EMS-Tac', value: 9 },
  { label: '11 - Interop', value: 11 },
  { label: '12 - Hospital', value: 12 },
  { label: '13 - Ham', value: 13 },
  { label: '14 - Public Works', value: 14 },
  { label: '15 - Aircraft', value: 15 },
  { label: '16 - Federal', value: 16 },
  { label: '17 - Business', value: 17 },
  { label: '20 - Railroad', value: 20 },
  { label: '21 - Other', value: 21 },
  { label: '22 - Multi-Talk', value: 22 },
  { label: '23 - Law Talk', value: 23 },
  { label: '24 - Fire-Talk', value: 24 },
  { label: '25 - EMS-Talk', value: 25 },
  { label: '26 - Transportation', value: 26 },
  { label: '29 - Emergency Ops', value: 29 },
  { label: '30 - Military', value: 30 },
  { label: '31 - Media', value: 31 },
  { label: '32 - Schools', value: 32 },
  { label: '33 - Security', value: 33 },
  { label: '34 - Utilities', value: 34 },
  { label: '37 - Corrections', value: 37 },
  { label: '208 - Custom 1', value: 208 },
  { label: '209 - Custom 2', value: 209 },
  { label: '210 - Custom 3', value: 210 },
  { label: '211 - Custom 4', value: 211 },
  { label: '212 - Custom 5', value: 212 },
  { label: '213 - Custom 6', value: 213 },
  { label: '214 - Custom 7', value: 214 },
  { label: '215 - Custom 8', value: 215 },
  { label: '216 - Racing Officials', value: 216 },
  { label: '217 - Racing Teams', value: 217 }
]

const showSystemDialog = ref(false)
const isEditSystemMode = ref(false)
const systemTypeOptions = [
  'Conventional',
  'Motorola',
  'Edacs',
  'Scat',
  'Ltr',
  'P25Standard',
  'P25OneFrequency',
  'P25X2_TDMA',
  'MotoTrbo',
  'DmrOneFrequency',
  'Nxdn',
  'NxdnOneFrequency'
]
const newSystem = ref({
  id: null,
  system_name: '',
  avoid: 'Off',
  system_type: 'Conventional',
  id_search: 'Off',
  emergency_alert: 'Off',
  emergency_alert_light: 'Off',
  status_bit: 'Ignore',
  p25_nac: 'Srch',
  quick_key: 'Off',
  number_tag: 'Off',
  hold_time: 0,
  priority_id_scan: 'Off',
  end_code: 'Analog',
  nxdn_format: '',
  analog_agc: 'Off',
  digital_agc: 'Off',
  digital_waiting_time: 400,
  digital_threshold_mode: 'Manual',
  digital_threshold_level: 8
})

const showDepartmentDialog = ref(false)
const isEditDepartmentMode = ref(false)
const newDepartment = ref({
  id: null,
  name_tag: '',
  avoid: 'Off',
  location_type: 'Circle',
  latitude: null,
  longitude: null,
  range_miles: null,
  quick_key: 'Off',
  system_type: 'Conventional'
})

const showEditFavoritesDialog = ref(false)
const editingFavorites = ref({
  id: null,
  user_name: ''
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
  if (section && ['favorites'].includes(section)) {
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
  loadFavoritesList()
})

onBeforeUnmount(() => {
  stopHpdbImportPolling()
})

// Auto-select the root node when favorites tree loads
watch(favoritesTreeNodes, (nodes) => {
  if (nodes && nodes.length > 0 && nodes[0].type === 'root') {
    selectedFavoritesNode.value = nodes[0]
    selectedFavoritesNodeId.value = nodes[0].id
  }
}, { immediate: true })

// Watch for section changes and reload favorites when needed
watch(activeSection, (newSection) => {
  if (newSection === 'favorites') {
    loadFavoritesList()
  }
})

const loadStats = async () => {
  statsLoading.value = true
  try {
    const [hpdbResp, favResp] = await Promise.all([
      api.get('/hpdb/stats/'),
      api.get('/favourites/stats/')
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
    const { data } = await api.get('/favourites/favorites-lists/')
    // Handle paginated response
    let favList = Array.isArray(data) ? data : (data.results || [])
    console.log('[DEBUG] Loaded', favList.length, 'favorites from API')
    
    // Sort by filename
    favList.sort((a, b) => (a.filename || '').localeCompare(b.filename || ''))
    
    // Load detailed info (groups/channels) for each favorite
    const favListsWithDetails = await Promise.all(
      favList.map(async (fav) => {
        try {
          const { data: detailData } = await api.get(`/favourites/favorites-lists/${fav.id}/detail/`)
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
  
  if (node.type === 'root') {
    // Root node - show multi-export view
    selectedFavoritesListIds.value = []
    return
  }
  
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
        const { data } = await api.get(`/favourites/cgroups/${groupId}/`)
        // Store frequencies in the node's groupData (normalize fields for UI)
        node.groupData.channels = (data.frequencies || []).map(freq => ({
          ...freq,
          audio_option: freq.audio_option || '',
          func_tag_id: freq.func_tag_id ?? 21,
          alert_light: freq.alert_light || freq.alert_color || 'Off',
          p_ch: freq.p_ch || freq.priority_channel || 'Off'
        }))
        console.log('[selectFavoritesNode] Loaded', data.frequencies?.length || 0, 'frequencies')
      } else if (systemType === 'Trunked') {
        const { data } = await api.get(`/favourites/tgroups/${groupId}/`)
        // Store TGIDs as channels in the node's groupData
        node.groupData.channels = (data.tgids || []).map(tgid => ({
          id: tgid.id,
          name_tag: tgid.name_tag,
          avoid: tgid.avoid,
          frequency: tgid.tgid,  // Use TGID value as "frequency" for display
          modulation: tgid.audio_type,
          audio_option: '',  // TGIDs don't have audio_option
          func_tag_id: tgid.func_tag_id,
          attenuator: '',  // TGIDs don't have attenuator
          delay: tgid.delay,
          alert_tone: tgid.alert_tone,
          alert_light: tgid.alert_color,
          volume_offset: tgid.volume_offset,
          number_tag: tgid.number_tag,
          priority_channel: tgid.priority_channel
        }))
        console.log('[selectFavoritesNode] Loaded', data.tgids?.length || 0, 'TGIDs')
      }
    } catch (error) {
      console.error('[selectFavoritesNode] Error loading channels:', error)
      $q.notify({ type: 'negative', message: 'Failed to load channels' })
    }
  } else if (node.type === 'system') {
    // System node selected - load and display departments (CGroups or TGroups)
    const favData = node.favData
    selectedFavoritesList.value = favData

    if (!systemsData.value?.length && favData?.id) {
      try {
        const { data } = await api.get(`/favourites/favorites-lists/${favData.id}/get-systems/`)
        systemsData.value = data.systems || []
      } catch (error) {
        console.error('[selectFavoritesNode] Error loading systems for id lookup:', error)
      }
    }

    if (!node.systemId && systemsData.value?.length) {
      const matched = systemsData.value.find(sys =>
        sys.system_name === node.system_name && sys.system_type === node.system_type
      )
      if (matched) {
        node.systemId = matched.id
      }
    }
    
    // Load departments for this system
    try {
      departmentsLoading.value = true
      
      // node.children contains the departments for this system
      if (node.children && node.children.length > 0) {
        departmentsData.value = node.children
          .filter(dept => !dept.groupData?.is_system_placeholder)  // Filter out placeholder departments
          .map(dept => ({
            id: dept.groupId,
            name_tag: dept.label.split(' (')[0], // Extract name without count
            avoid: dept.groupData?.avoid || 'Off',
            system_type: dept.system_type,
            location_type: dept.groupData?.location_type || 'Circle',
            quick_key: dept.groupData?.quick_key || 'Off',
            latitude: dept.groupData?.latitude ?? null,
            longitude: dept.groupData?.longitude ?? null,
            range_miles: dept.groupData?.range_miles ?? null
          }))
        console.log('[selectFavoritesNode] Loaded', departmentsData.value.length, 'departments for system')
      } else {
        departmentsData.value = []
      }
    } catch (error) {
      console.error('[selectFavoritesNode] Error loading departments:', error)
      $q.notify({ type: 'negative', message: 'Failed to load departments' })
    } finally {
      departmentsLoading.value = false
    }
  } else if (node.type === 'favorites_list') {
    // Set the favorites list directly
    selectedFavoritesList.value = node.favData
    
    // Load systems (ConventionalSystem and TrunkSystem) for this favorites list
    try {
      systemsLoading.value = true
      const { data } = await api.get(`/favourites/favorites-lists/${node.favData.id}/get-systems/`)
      systemsData.value = data.systems || []
      console.log('[selectFavoritesNode] Loaded', data.systems?.length || 0, 'systems')
    } catch (error) {
      console.error('[selectFavoritesNode] Error loading systems:', error)
      $q.notify({ type: 'negative', message: 'Failed to load systems' })
    } finally {
      systemsLoading.value = false
    }
  }
}

const getFavoritesNodeIcon = (node) => {
  switch (node.type) {
    case 'root': return 'star'
    case 'favorites_list': return 'bookmark'
    case 'system': return 'hub'
    case 'department': return 'radio'
    default: return 'circle'
  }
}

const getFavoritesNodeColor = (node) => {
  switch (node.type) {
    case 'root': return 'amber'
    case 'favorites_list': return 'orange'
    case 'system': return 'purple'
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
        console.log('[LAZY-LOAD] Fetching from:', `/favourites/cgroups/${groupId}/`)
        const { data } = await api.get(`/favourites/cgroups/${groupId}/`)
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
        console.log('[LAZY-LOAD] Fetching from:', `/favourites/tgroups/${groupId}/`)
        const { data } = await api.get(`/favourites/tgroups/${groupId}/`)
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
    await api.post('/favourites/clear-data/')
    console.log('[DEBUG] Data cleared')

    // Prepare form data
    const totalBytes = files.reduce((sum, file) => sum + file.size, 0)
    const formData = new FormData()
    files.forEach(file => formData.append('files', file))

    // Upload and import
    console.log('[DEBUG] Starting import upload...')
    const { data } = await axios.post(
      api.defaults.baseURL + '/favourites/import-files/',
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
      api.post('/favourites/clear-raw-data/')
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
      api.post('/favourites/clear-data/')
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

// Multi-favorite list export/import functions
const toggleFavoritesListSelection = (favId) => {
  const idx = selectedFavoritesListIds.value.indexOf(favId)
  if (idx > -1) {
    selectedFavoritesListIds.value.splice(idx, 1)
  } else {
    selectedFavoritesListIds.value.push(favId)
  }
}

const toggleAllFavoritesLists = (checked) => {
  if (checked) {
    selectedFavoritesListIds.value = favorites.value.map(f => f.id)
  } else {
    selectedFavoritesListIds.value = []
  }
}

const selectAllFavoritesLists = () => {
  selectedFavoritesListIds.value = favorites.value.map(f => f.id)
}

const clearFavoritesListSelection = () => {
  selectedFavoritesListIds.value = []
}

const exportSelectedFavoritesLists = async () => {
  try {
    if (selectedFavoritesListIds.value.length === 0) {
      $q.notify({ type: 'warning', message: 'Please select at least one favorites list' })
      return
    }

    const response = await api.post('/favourites/favorites-lists/export-json-multiple/', {
      ids: selectedFavoritesListIds.value
    }, { responseType: 'blob' })

    const blob = new Blob([response.data], { type: 'application/json' })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `favorites_lists_export_${Date.now()}.json`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)

    $q.notify({ type: 'positive', message: `Exported ${selectedFavoritesListIds.value.length} favorites list(s) to JSON` })
  } catch (error) {
    $q.notify({ type: 'negative', message: 'Export failed: ' + (error.response?.data?.error || error.message) })
  }
}

const importFavoritesJSON = async () => {
  return new Promise((resolve) => {
    const input = document.createElement('input')
    input.type = 'file'
    input.accept = '.json'
    input.onchange = async (e) => {
      const file = e.target.files[0]
      if (!file) {
        resolve()
        return
      }

      try {
        const formData = new FormData()
        formData.append('file', file)

        // Use a dummy ID since import creates new lists
        const { data } = await api.post('/favourites/favorites-lists/00000000000000000000000/import-json/', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })

        if (data.success) {
          $q.notify({ 
            type: 'positive', 
            message: `Imported ${data.imported} favorites list(s) from JSON` 
          })
          await loadFavoritesList()
        } else {
          const errorMsg = data.errors?.length > 0 ? `${data.errors[0]}` : 'Import failed'
          $q.notify({ type: 'negative', message: `JSON import failed: ${errorMsg}` })
        }
      } catch (error) {
        $q.notify({ type: 'negative', message: 'JSON import error: ' + (error.response?.data?.error || error.message) })
      }
      resolve()
    }
    input.click()
  })
}

const deleteSelectedFavoritesLists = () => {
  if (selectedFavoritesListIds.value.length === 0) {
    $q.notify({ type: 'warning', message: 'Please select at least one favorites list to delete' })
    return
  }

  const selectedCount = selectedFavoritesListIds.value.length
  const selectedFavs = favorites.value.filter(f => selectedFavoritesListIds.value.includes(f.id))
  let totalDepartments = 0
  let totalChannels = 0

  selectedFavs.forEach(fav => {
    totalDepartments += fav.groups ? fav.groups.length : 0
    if (fav.groups) {
      fav.groups.forEach(group => {
        totalChannels += group.freq_count || 0
      })
    }
  })

  // Show confirmation dialog
  $q.dialog({
    title: 'Delete Favorites Lists',
    message: `<strong style="color: #c41c3b;">⚠️ Warning: This action cannot be undone!</strong><br><br>
              You are about to delete <strong>${selectedCount}</strong> favorites list(s):<br><br>
              This will permanently delete:<br>
              • <strong>${totalDepartments}</strong> department(s)<br>
              • <strong>${totalChannels}</strong> channel(s)<br><br>
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
      let deletedCount = 0
      let failedCount = 0

      for (const favId of selectedFavoritesListIds.value) {
        try {
          await api.delete(`/favourites/favorites-lists/${favId}/`)
          deletedCount++
        } catch (error) {
          console.error(`Error deleting favorites list ${favId}:`, error)
          failedCount++
        }
      }

      if (deletedCount > 0) {
        $q.notify({ 
          type: 'positive', 
          message: `Deleted ${deletedCount} favorites list(s)` + (failedCount > 0 ? ` (${failedCount} failed)` : '') 
        })
      }
      if (failedCount > 0 && deletedCount === 0) {
        $q.notify({ type: 'negative', message: `Failed to delete ${failedCount} favorites list(s)` })
      }

      selectedFavoritesListIds.value = []
      selectedFavoritesNode.value = null
      selectedFavoritesNodeId.value = null
      await loadFavoritesList()
    } catch (error) {
      console.error('Error deleting favorites lists:', error)
      $q.notify({ type: 'negative', message: 'Failed to delete favorites lists' })
    }
  })
}

const exportFavoritesFolder = async () => {
  try {
    const response = await api.get('/favourites/export-favorites/', { responseType: 'blob' })
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

const exportFavoritesListCSV = async (favoritesList) => {
  try {
    const response = await api.get(`/favourites/favorites-lists/${favoritesList.id}/export-csv/`, { responseType: 'blob' })
    const blob = new Blob([response.data], { type: 'text/csv' })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `${favoritesList.user_name || 'favorites'}.csv`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)

    $q.notify({ type: 'positive', message: 'Favourites List CSV exported' })
  } catch (error) {
    $q.notify({ type: 'negative', message: 'CSV export failed: ' + (error.response?.data?.error || error.message) })
  }
}

const importFavoritesListCSV = async (favoritesList) => {
  return new Promise((resolve) => {
    const input = document.createElement('input')
    input.type = 'file'
    input.accept = '.csv'
    input.onchange = async (e) => {
      const file = e.target.files[0]
      if (!file) {
        resolve()
        return
      }

      try {
        const formData = new FormData()
        formData.append('file', file)

        const { data } = await api.post(`/favourites/favorites-lists/${favoritesList.id}/import-csv/`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })

        if (data.success) {
          $q.notify({ 
            type: 'positive', 
            message: `Imported ${data.imported} items from CSV` 
          })
          await loadFavoritesList()
        } else {
          const errorMsg = data.errors?.length > 0 ? `${data.errors[0]}` : 'Import failed'
          $q.notify({ type: 'negative', message: `CSV import failed: ${errorMsg}` })
        }
      } catch (error) {
        $q.notify({ type: 'negative', message: 'CSV import error: ' + (error.response?.data?.error || error.message) })
      }
      resolve()
    }
    input.click()
  })
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
  newFavoritesList.value = {
    user_name: '',
    location_control: 'Off',
    monitor: 'On',
    quick_key: 'Off',
    number_tag: 'Off',
    s_qkeys: Array(100).fill('Off'),
    startup_keys: Array(10).fill('Off')
  }
  isEditFavoritesListMode.value = false
  showCreateFavoritesListDialog.value = true
}

const normalizeOnOffArray = (arr) => {
  if (!Array.isArray(arr)) return arr
  return arr.map(val => {
    if (typeof val === 'boolean') {
      return val ? 'On' : 'Off'
    }
    if (typeof val === 'string') {
      return (val === 'On' || val === 'true' || val === '1') ? 'On' : 'Off'
    }
    return 'Off'
  })
}

const editFavoritesList = (favoritesList) => {
  newFavoritesList.value = {
    id: favoritesList.id,
    user_name: favoritesList.user_name,
    location_control: favoritesList.location_control,
    monitor: favoritesList.monitor,
    quick_key: favoritesList.quick_key,
    number_tag: favoritesList.number_tag,
    s_qkeys: normalizeOnOffArray(favoritesList.s_qkeys) || Array(100).fill('Off'),
    startup_keys: normalizeOnOffArray(favoritesList.startup_keys) || Array(10).fill('Off')
  }
  isEditFavoritesListMode.value = true
  showCreateFavoritesListDialog.value = true
}

const updateFavoritesList = async () => {
  if (!newFavoritesList.value.user_name || newFavoritesList.value.user_name.trim() === '') {
    $q.notify({ type: 'warning', message: 'Please enter a Favorite List Name' })
    return
  }

  try {
    await api.patch(`/favourites/favorites-lists/${newFavoritesList.value.id}/`, {
      user_name: newFavoritesList.value.user_name,
      location_control: newFavoritesList.value.location_control,
      monitor: newFavoritesList.value.monitor,
      quick_key: newFavoritesList.value.quick_key,
      number_tag: newFavoritesList.value.number_tag,
      s_qkeys: newFavoritesList.value.s_qkeys,
      startup_keys: newFavoritesList.value.startup_keys
    })

    $q.notify({ type: 'positive', message: 'Favorites list updated successfully!' })
    showCreateFavoritesListDialog.value = false
    isEditFavoritesListMode.value = false
    await loadFavoritesList()
  } catch (error) {
    console.error('Error updating favorites list:', error)
    $q.notify({ type: 'negative', message: 'Failed to update favorites list' })
  }
}

const submitCreateFavoritesList = async () => {
  if (!newFavoritesList.value.user_name || newFavoritesList.value.user_name.trim() === '') {
    $q.notify({ type: 'warning', message: 'Please enter a Favorite List Name' })
    return
  }

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

    const response = await api.post('/favourites/favorites-lists/', {
      user_name: newFavoritesList.value.user_name,
      filename: filename,
      location_control: newFavoritesList.value.location_control,
      monitor: newFavoritesList.value.monitor,
      quick_key: newFavoritesList.value.quick_key,
      number_tag: newFavoritesList.value.number_tag,
      s_qkeys: newFavoritesList.value.s_qkeys,
      startup_keys: newFavoritesList.value.startup_keys
    })

    $q.notify({ type: 'positive', message: 'Favorites list created successfully!' })
    showCreateFavoritesListDialog.value = false
    await loadFavoritesList()
  } catch (error) {
    console.error('Error creating favorites list:', error)
    $q.notify({ type: 'negative', message: 'Failed to create favorites list' })
  }
}

const deleteSingleFavoritesList = async (favoritesList) => {
  const listName = favoritesList.user_name
  const departmentCount = favoritesList.groups ? favoritesList.groups.length : 0
  let channelCount = 0
  if (favoritesList.groups) {
    favoritesList.groups.forEach(group => {
      channelCount += group.freq_count || 0
    })
  }
  
  // Show confirmation dialog with warning
  $q.dialog({
    title: 'Delete Favorites List',
    message: `<strong style="color: #c41c3b;">⚠️ Warning: This action cannot be undone!</strong><br><br>
              You are about to delete:<br>
              <strong>${listName}</strong><br><br>
              This will permanently delete:<br>
              • <strong>${departmentCount}</strong> department(s)<br>
              • <strong>${channelCount}</strong> channel(s)`,
    html: true,
    cancel: true,
    persistent: true
  }).onOk(async () => {
    try {
      await api.delete(`/favourites/favorites-lists/${favoritesList.id}/`)
      $q.notify({ type: 'positive', message: 'Favorites list deleted successfully!' })
      await loadFavoritesList()
    } catch (error) {
      console.error('Error deleting favorites list:', error)
      $q.notify({ type: 'negative', message: 'Failed to delete favorites list' })
    }
  })
}

const selectAllSQkeys = (value) => {
  newFavoritesList.value.s_qkeys = Array(100).fill(value ? 'On' : 'Off')
}

const selectAllStartupKeys = (value) => {
  newFavoritesList.value.startup_keys = Array(10).fill(value ? 'On' : 'Off')
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
      await api.delete(`/favourites/favorites-lists/${selectedFav.id}/`)
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
  try {
    // Validate we have a selected department
    if (!selectedFavoritesNode.value || selectedFavoritesNode.value.type !== 'department') {
      $q.notify({ type: 'negative', message: 'Please select a department to add channel to' })
      return
    }

    const systemType = selectedFavoritesNode.value.system_type
    const groupId = selectedFavoritesNode.value.groupId

    if (!isTrunkSystemType(systemType)) {
      // Validate frequency for conventional
      if (!newChannel.value.frequency || newChannel.value.frequency <= 0) {
        $q.notify({ type: 'negative', message: 'Frequency must be a positive integer (Hz)' })
        return
      }
      if (!newChannel.value.name_tag || newChannel.value.name_tag.trim() === '') {
        $q.notify({ type: 'negative', message: 'Channel name is required' })
        return
      }
      if (newChannel.value.name_tag.length > 64) {
        $q.notify({ type: 'negative', message: 'Channel name must be 64 characters or less' })
        return
      }

      // POST to add frequency
      const payload = {
        name_tag: newChannel.value.name_tag,
        frequency: Math.round(Number(newChannel.value.frequency) * 1000000),  // Convert MHz to Hz
        modulation: newChannel.value.modulation || 'AUTO',
        avoid: newChannel.value.avoid || 'Off',
        audio_option: newChannel.value.audio_option || '',
        func_tag_id: newChannel.value.func_tag_id || 21,
        attenuator: newChannel.value.attenuator || 'Off',
        delay: newChannel.value.delay || 2,
        volume_offset: newChannel.value.volume_offset || 0,
        alert_tone: newChannel.value.alert_tone || 'Off',
        alert_volume: newChannel.value.alert_volume || 'Auto',
        alert_color: newChannel.value.alert_color || 'Off',
        alert_pattern: newChannel.value.alert_pattern || 'On',
        number_tag: newChannel.value.number_tag || 'Off',
        priority_channel: newChannel.value.p_ch || 'Off'
      }

      await api.post(`/favourites/cgroups/${groupId}/add-frequency/`, payload)
      $q.notify({ type: 'positive', message: `Frequency "${newChannel.value.name_tag}" added successfully!` })
    } else if (isTrunkSystemType(systemType)) {
      // Validate TGID for trunked
      if (!newChannel.value.frequency || String(newChannel.value.frequency).trim() === '') {
        $q.notify({ type: 'negative', message: 'TGID is required' })
        return
      }
      if (!newChannel.value.name_tag || newChannel.value.name_tag.trim() === '') {
        $q.notify({ type: 'negative', message: 'TGID name is required' })
        return
      }

      // POST to add TGID
      const payload = {
        name_tag: newChannel.value.name_tag,
        tgid: String(newChannel.value.frequency),
        audio_type: newChannel.value.modulation || 'ALL',
        func_tag_id: newChannel.value.func_tag_id || 21,
        avoid: newChannel.value.avoid || 'Off',
        delay: newChannel.value.delay || 2,
        volume_offset: newChannel.value.volume_offset || 0,
        alert_tone: newChannel.value.alert_tone || 'Off',
        alert_volume: newChannel.value.alert_volume || 'Auto',
        alert_color: newChannel.value.alert_color || 'Off',
        alert_pattern: newChannel.value.alert_pattern || 'On',
        number_tag: newChannel.value.number_tag || 'Off',
        priority_channel: newChannel.value.p_ch || 'Off',
        tdma_slot: newChannel.value.tdma_slot || 'Any'
      }

      await api.post(`/favourites/tgroups/${groupId}/add-tgid/`, payload)
      $q.notify({ type: 'positive', message: `TGID "${newChannel.value.name_tag}" added successfully!` })
    }

    // Reset form
    newChannel.value.name_tag = ''
    newChannel.value.avoid = 'Off'
    newChannel.value.frequency = ''
    newChannel.value.modulation = 'AUTO'
    newChannel.value.audio_option = ''
    newChannel.value.func_tag_id = 21  // Reset to Other
    newChannel.value.delay = 15
    newChannel.value.attenuator = 'Off'
    newChannel.value.alert_tone = 'Off'
    newChannel.value.alert_color = 'Off'
    newChannel.value.alert_pattern = 'On'
    newChannel.value.volume_offset = '0'
    newChannel.value.p_ch = 'Off'
    newChannel.value.number_tag = null
    newChannel.value.priority = 0
    newChannel.value.enabled = true
    newChannel.value.tdma_slot = 'Any'

    // Close dialog
    showAddChannelDialog.value = false

    // Reload favorites list to update tree
    await loadFavoritesList()
    // Re-select the node to refresh its details
    if (selectedFavoritesNode.value?.id) {
      await selectFavoritesNode(selectedFavoritesNode.value)
    }

  } catch (error) {
    console.error('Error adding channel:', error)
    const errorMsg = error.response?.data?.detail || error.response?.data?.error || error.message || 'Failed to add channel'
    $q.notify({ type: 'negative', message: errorMsg })
  }
}

const openAddSystemDialog = () => {
  newSystem.value = {
    id: null,
    system_name: '',
    avoid: 'Off',
    system_type: 'Conventional',
    id_search: 'Off',
    emergency_alert: 'Off',
    emergency_alert_light: 'Off',
    status_bit: 'Ignore',
    p25_nac: 'Srch',
    quick_key: 'Off',
    number_tag: 'Off',
    hold_time: 0,
    priority_id_scan: 'Off',
    end_code: 'Analog',
    nxdn_format: '',
    analog_agc: 'Off',
    digital_agc: 'Off',
    digital_waiting_time: 400,
    digital_threshold_mode: 'Manual',
    digital_threshold_level: 8
  }
  isEditSystemMode.value = false
  showSystemDialog.value = true
}

const editSystem = (system) => {
  newSystem.value = {
    id: system.id,
    system_name: system.system_name || system.name || '',
    avoid: system.avoid || 'Off',
    system_type: system.system_type || 'Conventional',
    id_search: system.id_search || 'Off',
    emergency_alert: system.emergency_alert || 'Off',
    emergency_alert_light: system.emergency_alert_light || 'Off',
    status_bit: system.status_bit || 'Ignore',
    p25_nac: system.p25_nac || 'Srch',
    quick_key: system.quick_key || 'Off',
    number_tag: system.number_tag || 'Off',
    hold_time: system.hold_time || 0,
    priority_id_scan: system.priority_id_scan || 'Off',
    end_code: system.end_code || 'Analog',
    nxdn_format: system.nxdn_format || '',
    analog_agc: system.analog_agc || 'Off',
    digital_agc: system.digital_agc || 'Off',
    digital_waiting_time: system.digital_waiting_time || 400,
    digital_threshold_mode: system.digital_threshold_mode || 'Manual',
    digital_threshold_level: system.digital_threshold_level || 8
  }
  isEditSystemMode.value = true
  showSystemDialog.value = true
}

const deleteSystem = async (system) => {
  const systemName = system.system_name || 'this system'
  
  try {
    // Fetch system details to get accurate counts
    let departmentCount = 0
    let channelCount = 0
    
    try {
      const isConventional = system.system_type === 'Conventional'
      const endpoint = isConventional 
        ? `/favourites/conventional-systems/${system.id}/`
        : `/favourites/trunk-systems/${system.id}/`
      
      const { data } = await api.get(endpoint)
      
      // Count departments and channels
      if (data.groups && Array.isArray(data.groups)) {
        departmentCount = data.groups.length
        data.groups.forEach(group => {
          const freqCount = isConventional 
            ? group.frequencies?.length || 0
            : group.tgids?.length || 0
          channelCount += freqCount
        })
      }
    } catch (error) {
      console.warn('Could not fetch system details for counts:', error)
    }
    
    const departmentText = departmentCount === 1 ? '1 Department' : `${departmentCount} Departments`
    const channelText = channelCount === 1 ? '1 Channel' : `${channelCount} Channels`
    
    $q.dialog({
      title: 'Delete System',
      message: `<strong style="color: #c41c3b;">⚠️ Warning: This action cannot be undone!</strong><br><br>
                You are about to delete:<br>
                <strong>${systemName}</strong><br><br>
                This will permanently delete:<br>
                • <strong>${departmentText}</strong><br>
                • <strong>${channelText}</strong>`,
      html: true,
      cancel: true,
      persistent: true
    }).onOk(async () => {
      try {
        // Determine if it's a ConventionalSystem or TrunkSystem based on system_type
        const isConventional = system.system_type === 'Conventional'
        const apiEndpoint = isConventional 
          ? `/favourites/conventional-systems/${system.id}/`
          : `/favourites/trunk-systems/${system.id}/`
        
        await api.delete(apiEndpoint)
        
        $q.notify({ type: 'positive', message: 'System deleted successfully!' })
        
        // Remove from local array immediately
        systemsData.value = systemsData.value.filter(s => s.id !== system.id)
        
        // Reload the tree and systems
        await loadFavoritesList()
      } catch (error) {
        console.error('[deleteSystem] Error deleting system:', error)
        $q.notify({ type: 'negative', message: 'Failed to delete system: ' + (error.response?.data?.detail || error.message) })
      }
    })
  } catch (error) {
    console.error('[deleteSystem] Error:', error)
    $q.notify({ type: 'negative', message: 'Error preparing delete: ' + error.message })
  }
}

const addSystemToFavorites = async () => {
  if (!newSystem.value.system_name || newSystem.value.system_name.trim() === '') {
    $q.notify({ type: 'negative', message: 'System name is required' })
    return
  }

  try {
    const favoritesList = selectedFavoritesNode.value?.type === 'favorites_list'
      ? selectedFavoritesNode.value.favData
      : selectedFavoritesList.value

    if (!favoritesList || !favoritesList.id) {
      $q.notify({ type: 'negative', message: 'Please select a favorites list to add system to' })
      return
    }

    const payload = {
      name_tag: newSystem.value.system_name,
      avoid: newSystem.value.avoid,
      system_type: newSystem.value.system_type,
      id_search: newSystem.value.id_search,
      emergency_alert: newSystem.value.emergency_alert,
      emergency_alert_light: newSystem.value.emergency_alert_light,
      status_bit: newSystem.value.status_bit,
      p25_nac: newSystem.value.p25_nac,
      quick_key: newSystem.value.quick_key,
      number_tag: newSystem.value.number_tag,
      priority_id_scan: newSystem.value.priority_id_scan,
      end_code: newSystem.value.end_code,
      nxdn_format: newSystem.value.nxdn_format,
      analog_agc: newSystem.value.analog_agc,
      digital_agc: newSystem.value.digital_agc,
      digital_waiting_time: newSystem.value.digital_waiting_time,
      digital_threshold_mode: newSystem.value.digital_threshold_mode,
      digital_threshold_level: newSystem.value.digital_threshold_level
    }

    if (!isTrunkSystemType(newSystem.value.system_type)) {
      payload.system_hold_time = newSystem.value.hold_time
    } else {
      payload.site_hold_time = newSystem.value.hold_time
    }

    await api.post(`/favourites/favorites-lists/${favoritesList.id}/add-system/`, payload)
    $q.notify({ type: 'positive', message: `System "${newSystem.value.system_name}" added successfully!` })

    showSystemDialog.value = false
    await loadFavoritesList()
    await selectFavoritesNode({ ...selectedFavoritesNode.value, type: 'favorites_list', favData: favoritesList })
  } catch (error) {
    console.error('Error adding system:', error)
    const errorMsg = error.response?.data?.detail || error.response?.data?.error || error.message || 'Failed to add system'
    $q.notify({ type: 'negative', message: errorMsg })
  }
}

const updateSystem = async () => {
  if (!newSystem.value.system_name || newSystem.value.system_name.trim() === '') {
    $q.notify({ type: 'negative', message: 'System name is required' })
    return
  }

  try {
    if (!isTrunkSystemType(newSystem.value.system_type)) {
      const payload = {
        name_tag: newSystem.value.system_name,
        avoid: newSystem.value.avoid,
        system_type: newSystem.value.system_type,
        quick_key: newSystem.value.quick_key,
        number_tag: newSystem.value.number_tag,
        system_hold_time: newSystem.value.hold_time,
        analog_agc: newSystem.value.analog_agc,
        digital_agc: newSystem.value.digital_agc,
        digital_waiting_time: newSystem.value.digital_waiting_time,
        digital_threshold_mode: newSystem.value.digital_threshold_mode,
        digital_threshold_level: newSystem.value.digital_threshold_level
      }

      await api.patch(`/favourites/conventional-systems/${newSystem.value.id}/`, payload)
    } else {
      const payload = {
        name_tag: newSystem.value.system_name,
        avoid: newSystem.value.avoid,
        system_type: newSystem.value.system_type,
        id_search: newSystem.value.id_search,
        alert_tone: newSystem.value.emergency_alert,
        alert_color: newSystem.value.emergency_alert_light,
        status_bit: newSystem.value.status_bit,
        nac: newSystem.value.p25_nac,
        quick_key: newSystem.value.quick_key,
        number_tag: newSystem.value.number_tag,
        site_hold_time: newSystem.value.hold_time,
        priority_id_scan: newSystem.value.priority_id_scan,
        end_code: newSystem.value.end_code,
        tgid_format: newSystem.value.nxdn_format,
        analog_agc: newSystem.value.analog_agc,
        digital_agc: newSystem.value.digital_agc
      }

      await api.patch(`/favourites/trunk-systems/${newSystem.value.id}/`, payload)
    }

    $q.notify({ type: 'positive', message: 'System updated successfully!' })
    showSystemDialog.value = false
    isEditSystemMode.value = false
    await selectFavoritesNode(selectedFavoritesNode.value)
  } catch (error) {
    console.error('Error updating system:', error)
    $q.notify({ type: 'negative', message: 'Failed to update system' })
  }
}

const openAddDepartmentDialog = () => {
  newDepartment.value = {
    id: null,
    name_tag: '',
    avoid: 'Off',
    location_type: 'Circle',
    latitude: null,
    longitude: null,
    range_miles: null,
    quick_key: 'Off',
    system_type: selectedFavoritesNode.value?.system_type || 'Conventional'
  }
  isEditDepartmentMode.value = false
  showDepartmentDialog.value = true
}

const editDepartment = (department) => {
  newDepartment.value = {
    id: department.id,
    name_tag: department.name_tag,
    avoid: department.avoid || 'Off',
    location_type: department.location_type || 'Circle',
    latitude: department.latitude ?? null,
    longitude: department.longitude ?? null,
    range_miles: department.range_miles ?? null,
    quick_key: department.quick_key || 'Off',
    system_type: selectedFavoritesNode.value?.system_type || department.system_type || 'Conventional'
  }
  isEditDepartmentMode.value = true
  showDepartmentDialog.value = true
}

const addDepartmentToSystem = async () => {
  if (!newDepartment.value.name_tag || newDepartment.value.name_tag.trim() === '') {
    $q.notify({ type: 'negative', message: 'Department name is required' })
    return
  }

  try {
    if (!selectedFavoritesNode.value || selectedFavoritesNode.value.type !== 'system') {
      $q.notify({ type: 'negative', message: 'Please select a system to add department to' })
      return
    }

    let systemId = selectedFavoritesNode.value.systemId || selectedFavoritesNode.value.id
    const systemType = selectedFavoritesNode.value.system_type || 'Conventional'

    if (!systemId && systemsData.value?.length) {
      const matched = systemsData.value.find(sys =>
        sys.system_name === selectedFavoritesNode.value.system_name &&
        sys.system_type === systemType
      )
      systemId = matched?.id
    }

    if (!systemId) {
      $q.notify({ type: 'negative', message: 'Unable to determine system id for department' })
      return
    }

    const payload = {
      name_tag: newDepartment.value.name_tag,
      avoid: newDepartment.value.avoid,
      latitude: newDepartment.value.latitude,
      longitude: newDepartment.value.longitude,
      range_miles: newDepartment.value.range_miles,
      location_type: newDepartment.value.location_type,
      quick_key: newDepartment.value.quick_key
    }

    if (!isTrunkSystemType(systemType)) {
      await api.post(`/favourites/conventional-systems/${systemId}/add-department/`, payload)
    } else {
      await api.post(`/favourites/trunk-systems/${systemId}/add-department/`, payload)
    }

    $q.notify({ type: 'positive', message: `Department "${newDepartment.value.name_tag}" added successfully!` })
    showDepartmentDialog.value = false
    await loadFavoritesList()
    // Re-select the system to show its details
    if (selectedFavoritesNode.value?.id) {
      await selectFavoritesNode(selectedFavoritesNode.value)
    }
  } catch (error) {
    console.error('Error adding department:', error)
    const errorMsg = error.response?.data?.detail || error.response?.data?.error || error.message || 'Failed to add department'
    $q.notify({ type: 'negative', message: errorMsg })
  }
}

const updateDepartment = async () => {
  if (!newDepartment.value.name_tag || newDepartment.value.name_tag.trim() === '') {
    $q.notify({ type: 'negative', message: 'Department name is required' })
    return
  }

  try {
    const payload = {
      name_tag: newDepartment.value.name_tag,
      avoid: newDepartment.value.avoid,
      location_type: newDepartment.value.location_type,
      latitude: newDepartment.value.latitude,
      longitude: newDepartment.value.longitude,
      range_miles: newDepartment.value.range_miles,
      quick_key: newDepartment.value.quick_key
    }

    if (!isTrunkSystemType(newDepartment.value.system_type)) {
      await api.patch(`/favourites/cgroups/${newDepartment.value.id}/`, payload)
    } else {
      await api.patch(`/favourites/tgroups/${newDepartment.value.id}/`, payload)
    }

    $q.notify({ type: 'positive', message: 'Department updated successfully!' })
    showDepartmentDialog.value = false
    isEditDepartmentMode.value = false
    await selectFavoritesNode(selectedFavoritesNode.value)
  } catch (error) {
    console.error('Error updating department:', error)
    $q.notify({ type: 'negative', message: 'Failed to update department' })
  }
}

const deleteDepartment = async (department) => {
  const departmentName = department.name_tag || 'this department'
  
  try {
    const systemType = selectedFavoritesNode.value?.system_type || department.system_type
    
    // Fetch department details to get accurate channel count
    let channelCount = 0
    try {
      if (systemType === 'Trunked') {
        const { data } = await api.get(`/favourites/tgroups/${department.id}/`)
        channelCount = data.tgids?.length || 0
      } else {
        const { data } = await api.get(`/favourites/cgroups/${department.id}/`)
        channelCount = data.frequencies?.length || 0
      }
    } catch (error) {
      console.warn('Could not fetch department details for channel count:', error)
    }
    
    const channelText = channelCount === 1 ? '1 channel' : `${channelCount} channels`
    
    $q.dialog({
      title: 'Delete Department',
      message: `Delete ${departmentName}? This will also delete ${channelText}. This cannot be undone.`,
      cancel: true,
      persistent: true
    }).onOk(async () => {
      try {
        if (systemType === 'Trunked') {
          await api.delete(`/favourites/tgroups/${department.id}/`)
        } else {
          await api.delete(`/favourites/cgroups/${department.id}/`)
        }

        $q.notify({ type: 'positive', message: 'Department deleted successfully!' })

        // Remove from local array immediately
        departmentsData.value = departmentsData.value.filter(d => d.id !== department.id)
        
        if (selectedFavoritesNode.value && selectedFavoritesNode.value.type === 'system') {
          await selectFavoritesNode(selectedFavoritesNode.value)
        }
      } catch (error) {
        console.error('[deleteDepartment] Error deleting department:', error)
        $q.notify({ type: 'negative', message: 'Failed to delete department: ' + (error.response?.data?.detail || error.message) })
      }
    })
  } catch (error) {
    console.error('[deleteDepartment] Error:', error)
    $q.notify({ type: 'negative', message: 'Error preparing delete: ' + error.message })
  }
}

const editChannel = (channel) => {
  // Populate newChannel with existing channel data
  // Convert frequency from Hz to MHz for display
  const freqValue = channel.frequency || channel.tgid
  const frequencyInKHz = !isTrunkSystemType(selectedFavoritesNode.value?.system_type) && freqValue 
    ? freqValue / 1000000 
    : freqValue
  
  // Helper function to convert string values to proper numeric defaults
  const toNumber = (value, defaultValue) => {
    const num = parseInt(value)
    return isNaN(num) ? defaultValue : num
  }
  
  newChannel.value = {
    id: channel.id || channel._id,
    name_tag: channel.name_tag,
    avoid: channel.avoid || 'Off',
    frequency: frequencyInKHz,
    modulation: channel.modulation || channel.audio_type || 'AUTO',
    audio_option: channel.audio_option || '',
    func_tag_id: channel.func_tag_id || 21,
    attenuator: channel.attenuator || 'Off',
    delay: toNumber(channel.delay, 2),
    alert_tone: channel.alert_tone || 'Off',
    alert_color: channel.alert_color || 'Off',
    alert_pattern: channel.alert_pattern || 'On',
    volume_offset: toNumber(channel.volume_offset, 0),
    number_tag: channel.number_tag || 'Off',
    p_ch: channel.p_ch || channel.priority_channel || 'Off',
    priority: toNumber(channel.priority, 0),
    enabled: channel.enabled !== false,
    tdma_slot: channel.tdma_slot || 'Any',
    system_type: selectedFavoritesNode.value?.system_type || 'Conventional'
  }
  console.log('[editChannel] Loaded channel:', {
    name: newChannel.value.name_tag,
    func_tag_id: newChannel.value.func_tag_id,
    original_func_tag_id: channel.func_tag_id
  })
  isEditMode.value = true
  showAddChannelDialog.value = true
}

const updateChannel = async () => {
  if (!newChannel.value.name_tag || newChannel.value.name_tag.trim() === '') {
    $q.notify({ type: 'negative', message: 'Channel name is required' })
    return
  }

  try {
    const payload = {
      name_tag: newChannel.value.name_tag,
      avoid: newChannel.value.avoid,
      modulation: newChannel.value.modulation,
      audio_option: newChannel.value.audio_option || '',
      func_tag_id: newChannel.value.func_tag_id,
      delay: newChannel.value.delay,
      volume_offset: newChannel.value.volume_offset,
      alert_tone: newChannel.value.alert_tone,
      number_tag: newChannel.value.number_tag,
      priority_channel: newChannel.value.p_ch
    }
    
    console.log('[updateChannel] Starting with payload.func_tag_id:', payload.func_tag_id)

    if (!isTrunkSystemType(newChannel.value.system_type)) {
      payload.frequency = Math.round(Number(newChannel.value.frequency) * 1000000)  // Convert MHz to Hz
      payload.attenuator = newChannel.value.attenuator
      payload.alert_volume = 'Auto'
      payload.alert_color = newChannel.value.alert_color
      payload.alert_pattern = newChannel.value.alert_pattern
      
      console.log('CFreq Update Payload:', payload)
      const response = await api.patch(`/favourites/cfreqs/${newChannel.value.id}/`, payload)
      console.log('CFreq Update Response:', response.data)
    } else {
      payload.tgid = newChannel.value.frequency
      payload.audio_type = newChannel.value.modulation
      payload.alert_volume = 'Auto'
      payload.alert_color = newChannel.value.alert_color
      payload.alert_pattern = newChannel.value.alert_pattern
      payload.tdma_slot = newChannel.value.tdma_slot || 'Any'
      
      await api.patch(`/favourites/tgids/${newChannel.value.id}/`, payload)
    }
    
    $q.notify({ type: 'positive', message: 'Channel updated successfully!' })
    showAddChannelDialog.value = false
    isEditMode.value = false
    
    console.log('[updateChannel] Update successful, reloading node')
    // Reload the channels for the current department
    if (selectedFavoritesNode.value && selectedFavoritesNode.value.type === 'department') {
      await selectFavoritesNode(selectedFavoritesNode.value)
    }
  } catch (error) {
    console.error('[updateChannel] Error updating channel:', error)
    if (error.response?.data) {
      console.error('[updateChannel] Error response data:', error.response.data)
    }
    $q.notify({ type: 'negative', message: 'Failed to update channel: ' + (error.response?.data?.detail || error.message) })
  }
}

const deleteChannel = (channel) => {
  const channelName = channel.name_tag || 'this channel'
  $q.dialog({
    title: 'Delete Channel',
    message: `Delete ${channelName}? This cannot be undone.`,
    cancel: true,
    persistent: true
  }).onOk(async () => {
    try {
      const systemType = selectedFavoritesNode.value?.system_type || channel.system_type

      if (systemType === 'Trunked') {
        await api.delete(`/favourites/tgids/${channel.id}/`)
      } else {
        await api.delete(`/favourites/cfreqs/${channel.id}/`)
      }

      $q.notify({ type: 'positive', message: 'Channel deleted successfully!' })

      if (selectedFavoritesNode.value && selectedFavoritesNode.value.type === 'department') {
        await selectFavoritesNode(selectedFavoritesNode.value)
      }
    } catch (error) {
      console.error('[deleteChannel] Error deleting channel:', error)
      $q.notify({ type: 'negative', message: 'Failed to delete channel: ' + (error.response?.data?.detail || error.message) })
    }
  })
}

const openAddChannelDialog = () => {
  // Reset form to default values
  newChannel.value = {
    id: null,
    name_tag: '',
    avoid: 'Off',
    frequency: '',
    modulation: 'AUTO',
    audio_option: '',
    func_tag_id: 21,
    attenuator: 'Off',
    delay: 2,
    alert_tone: 'Off',
    alert_color: 'Off',
    alert_pattern: 'On',
    volume_offset: 0,
    number_tag: 'Off',
    p_ch: 'Off',
    priority: 0,
    enabled: true,
    tdma_slot: 'Any',
    system_type: selectedFavoritesNode.value?.system_type || 'Conventional'
  }
  isEditMode.value = false
  showAddChannelDialog.value = true
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
