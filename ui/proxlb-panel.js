// Proxmox Load Balancer - Cemal Demirci
// github.com/cemal-demirci

(function() {
    'use strict';

    var DASHBOARD_URL, API_URL;

    function init() {
        DASHBOARD_URL = 'http://' + window.location.hostname + ':5000';
        API_URL = DASHBOARD_URL + '/api';

        console.log('ProxLB: Initializing...');

        // Wait for ExtJS to be ready
        if (typeof Ext === 'undefined') {
            setTimeout(init, 500);
            return;
        }

        // Wait for viewport to be ready
        Ext.onReady(function() {
            setTimeout(tryAddButton, 2000);
        });
    }

    function tryAddButton() {
        console.log('ProxLB: Trying to add button...');

        // Try to find toolbar with multiple methods
        var toolbar = null;
        var insertIndex = 2;

        // Method 1: Find viewport and get top toolbar
        try {
            var viewport = Ext.ComponentQuery.query('viewport')[0];
            if (viewport) {
                var toolbars = viewport.query('toolbar');
                for (var i = 0; i < toolbars.length; i++) {
                    var tb = toolbars[i];
                    if (tb.dock === 'top' && tb.items && tb.items.length > 5) {
                        // Check if this toolbar has the Documentation button
                        var hasDoc = false;
                        tb.items.each(function(item, idx) {
                            if (item.text === 'Documentation' || (item.iconCls && item.iconCls.indexOf('book') > -1)) {
                                hasDoc = true;
                                insertIndex = idx + 1;
                            }
                        });
                        if (hasDoc) {
                            toolbar = tb;
                            console.log('ProxLB: Found toolbar with Documentation button');
                            break;
                        }
                    }
                }
            }
        } catch(e) {
            console.log('ProxLB: Method 1 failed:', e);
        }

        // Method 2: Try component query
        if (!toolbar) {
            try {
                var tbars = Ext.ComponentQuery.query('toolbar[dock=top]');
                for (var j = 0; j < tbars.length; j++) {
                    if (tbars[j].items && tbars[j].items.length > 5) {
                        toolbar = tbars[j];
                        console.log('ProxLB: Found toolbar via query');
                        break;
                    }
                }
            } catch(e) {
                console.log('ProxLB: Method 2 failed:', e);
            }
        }

        if (toolbar && toolbar.items) {
            // Check if button already exists
            var exists = false;
            toolbar.items.each(function(item) {
                if (item.text === 'Load Balancer') {
                    exists = true;
                    return false;
                }
            });

            if (exists) {
                console.log('ProxLB: Button already exists');
                return;
            }

            // Create the Load Balancer button
            var lbButton = Ext.create('Ext.button.Button', {
                text: 'Load Balancer',
                iconCls: 'fa fa-balance-scale',
                cls: 'proxlb-btn',
                style: {
                    background: 'linear-gradient(135deg, #f97316, #ea580c)',
                    border: 'none',
                    borderRadius: '4px',
                    color: 'white'
                },
                menu: {
                    items: [
                        { text: 'Dashboard', iconCls: 'fa fa-chart-pie', handler: openDashboard },
                        { text: 'Ayarlar', iconCls: 'fa fa-cog', handler: openSettings },
                        '-',
                        { text: 'Yeni Sekmede Ac', iconCls: 'fa fa-external-link', handler: openExternal }
                    ]
                }
            });

            toolbar.insert(insertIndex, lbButton);
            console.log('ProxLB: Button added to toolbar at position ' + insertIndex);
        } else {
            console.log('ProxLB: Toolbar not found, using floating button');
            addFloatingButton();
        }
    }

    function addFloatingButton() {
        // Check if already added
        if (document.getElementById('proxlb-float-btn')) {
            return;
        }

        var style = document.createElement('style');
        style.textContent =
            '#proxlb-float-btn { position: fixed; top: 8px; right: 300px; z-index: 99999; ' +
            'padding: 8px 16px; border-radius: 4px; cursor: pointer; ' +
            'background: linear-gradient(135deg, #f97316, #ea580c); border: none; ' +
            'box-shadow: 0 2px 8px rgba(249,115,22,0.4); transition: all 0.3s; display: flex; ' +
            'align-items: center; gap: 8px; color: white; font-size: 13px; font-weight: 500; font-family: inherit; }' +
            '#proxlb-float-btn:hover { transform: scale(1.02); box-shadow: 0 4px 12px rgba(249,115,22,0.6); }' +
            '#proxlb-menu { position: fixed; top: 44px; right: 300px; z-index: 99998; ' +
            'background: #1e293b; border-radius: 6px; padding: 6px 0; min-width: 180px; ' +
            'box-shadow: 0 10px 40px rgba(0,0,0,0.5); display: none; border: 1px solid #334155; }' +
            '#proxlb-menu.show { display: block; }' +
            '.proxlb-menu-item { padding: 10px 16px; color: #e2e8f0; cursor: pointer; ' +
            'display: flex; align-items: center; gap: 10px; transition: background 0.2s; font-size: 13px; }' +
            '.proxlb-menu-item:hover { background: #334155; }' +
            '.proxlb-menu-item i { width: 20px; text-align: center; color: #f97316; font-size: 14px; }';
        document.head.appendChild(style);

        var btn = document.createElement('button');
        btn.id = 'proxlb-float-btn';
        btn.innerHTML = '<i class="fa fa-balance-scale"></i> Load Balancer';
        btn.onclick = function(e) {
            e.stopPropagation();
            var menu = document.getElementById('proxlb-menu');
            menu.classList.toggle('show');
        };
        document.body.appendChild(btn);

        var menu = document.createElement('div');
        menu.id = 'proxlb-menu';
        menu.innerHTML =
            '<div class="proxlb-menu-item" onclick="ProxLB.openDashboard()"><i class="fa fa-chart-pie"></i> Dashboard</div>' +
            '<div class="proxlb-menu-item" onclick="ProxLB.openSettings()"><i class="fa fa-cog"></i> Ayarlar</div>' +
            '<div class="proxlb-menu-item" onclick="ProxLB.openExternal()"><i class="fa fa-external-link"></i> Yeni Sekmede Ac</div>';
        document.body.appendChild(menu);

        document.addEventListener('click', function(e) {
            if (!e.target.closest('#proxlb-float-btn') && !e.target.closest('#proxlb-menu')) {
                document.getElementById('proxlb-menu').classList.remove('show');
            }
        });

        console.log('ProxLB: Floating button added');
    }

    function openDashboard() {
        // Close menu if open
        var menu = document.getElementById('proxlb-menu');
        if (menu) menu.classList.remove('show');

        if (typeof Ext !== 'undefined') {
            var win = Ext.create('Ext.window.Window', {
                title: 'Proxmox Load Balancer Dashboard',
                width: Math.min(1400, window.innerWidth - 100),
                height: Math.min(900, window.innerHeight - 100),
                layout: 'fit',
                maximizable: true,
                modal: false,
                items: [{
                    xtype: 'component',
                    autoEl: { tag: 'iframe', src: DASHBOARD_URL, style: 'width:100%;height:100%;border:none;' }
                }]
            });
            win.show();
        } else {
            window.open(DASHBOARD_URL, '_blank');
        }
    }

    function openSettings() {
        // Close menu if open
        var menu = document.getElementById('proxlb-menu');
        if (menu) menu.classList.remove('show');

        if (typeof Ext !== 'undefined') {
            var win = Ext.create('Ext.window.Window', {
                title: 'Load Balancer Ayarlari',
                iconCls: 'fa fa-cog',
                width: 650,
                height: 800,
                layout: 'fit',
                maximizable: true,
                modal: false,
                bodyPadding: 10,
                items: [{
                    xtype: 'form',
                    border: false,
                    bodyPadding: 15,
                    scrollable: true,
                    defaults: { anchor: '100%', labelWidth: 150 },
                    items: [
                        { xtype: 'fieldset', title: 'Genel Ayarlar', collapsible: true, defaults: { anchor: '100%', labelWidth: 150 }, items: [
                            { xtype: 'checkbox', fieldLabel: 'LB Aktif', name: 'enabled', checked: true },
                            { xtype: 'combo', fieldLabel: 'Mod', name: 'mode', store: [['memory','Memory'],['cpu','CPU'],['disk','Disk'],['storage','Storage'],['combined','Birlesik']], value: 'combined', editable: false },
                            { xtype: 'numberfield', fieldLabel: 'Fark Esigi (%)', name: 'threshold', value: 15, minValue: 5, maxValue: 50 },
                            { xtype: 'numberfield', fieldLabel: 'Kontrol Araligi (dk)', name: 'interval', value: 15, minValue: 5, maxValue: 60 },
                            { xtype: 'checkbox', fieldLabel: 'Dry Run (Test)', name: 'dry_run', checked: false }
                        ]},
                        { xtype: 'fieldset', title: 'CPU Dengeleme', collapsible: true, defaults: { anchor: '100%', labelWidth: 150 }, items: [
                            { xtype: 'checkbox', fieldLabel: 'CPU Aktif', name: 'cpu_enabled', checked: true },
                            { xtype: 'numberfield', fieldLabel: 'CPU Esik (%)', name: 'cpu_threshold', value: 80, minValue: 50, maxValue: 95 },
                            { xtype: 'numberfield', fieldLabel: 'CPU Agirlik', name: 'cpu_weight', value: 1.0, minValue: 0, maxValue: 5, step: 0.1 }
                        ]},
                        { xtype: 'fieldset', title: 'Bellek Dengeleme', collapsible: true, defaults: { anchor: '100%', labelWidth: 150 }, items: [
                            { xtype: 'checkbox', fieldLabel: 'RAM Aktif', name: 'memory_enabled', checked: true },
                            { xtype: 'numberfield', fieldLabel: 'RAM Esik (%)', name: 'memory_threshold', value: 85, minValue: 50, maxValue: 95 },
                            { xtype: 'numberfield', fieldLabel: 'RAM Agirlik', name: 'memory_weight', value: 2.0, minValue: 0, maxValue: 5, step: 0.1 },
                            { xtype: 'checkbox', fieldLabel: 'Balloon Aktif', name: 'balloon_enabled', checked: true },
                            { xtype: 'numberfield', fieldLabel: 'Min Balloon (%)', name: 'balloon_min', value: 50, minValue: 10, maxValue: 100 }
                        ]},
                        { xtype: 'fieldset', title: 'Disk Dengeleme', collapsible: true, defaults: { anchor: '100%', labelWidth: 150 }, items: [
                            { xtype: 'checkbox', fieldLabel: 'Disk Aktif', name: 'disk_enabled', checked: true },
                            { xtype: 'numberfield', fieldLabel: 'Disk Esik (%)', name: 'disk_threshold', value: 85, minValue: 50, maxValue: 95 },
                            { xtype: 'numberfield', fieldLabel: 'Disk Agirlik', name: 'disk_weight', value: 1.0, minValue: 0, maxValue: 5, step: 0.1 }
                        ]},
                        { xtype: 'fieldset', title: 'Storage Dengeleme', collapsible: true, defaults: { anchor: '100%', labelWidth: 150 }, items: [
                            { xtype: 'checkbox', fieldLabel: 'Storage Aktif', name: 'storage_enabled', checked: true },
                            { xtype: 'numberfield', fieldLabel: 'Storage Esik (%)', name: 'storage_threshold', value: 80, minValue: 50, maxValue: 95 },
                            { xtype: 'numberfield', fieldLabel: 'Storage Agirlik', name: 'storage_weight', value: 1.5, minValue: 0, maxValue: 5, step: 0.1 },
                            { xtype: 'textfield', fieldLabel: 'Izlenecek Storage', name: 'monitored_storages', emptyText: 'local-lvm,ceph,nfs (bos=hepsi)' }
                        ]},
                        { xtype: 'fieldset', title: 'Migrasyon', collapsible: true, defaults: { anchor: '100%', labelWidth: 150 }, items: [
                            { xtype: 'combo', fieldLabel: 'Tip', name: 'migration_type', store: [['online','Online (Canli)'],['offline','Offline (Durdur)']], value: 'online', editable: false },
                            { xtype: 'numberfield', fieldLabel: 'Esanli Migrasyon', name: 'max_migrations', value: 2, minValue: 1, maxValue: 5 },
                            { xtype: 'checkbox', fieldLabel: 'Lokal Disk Tasi', name: 'with_local_disks', checked: false },
                            { xtype: 'numberfield', fieldLabel: 'Bant Genisligi (MB/s)', name: 'migration_bandwidth', value: 0, minValue: 0, emptyText: '0 = Sinirsiz' },
                            { xtype: 'numberfield', fieldLabel: 'Timeout (sn)', name: 'migration_timeout', value: 300, minValue: 60, maxValue: 3600 }
                        ]},
                        { xtype: 'fieldset', title: 'Haric Tutulacaklar', collapsible: true, collapsed: true, defaults: { anchor: '100%', labelWidth: 150 }, items: [
                            { xtype: 'textfield', fieldLabel: 'VM IDleri', name: 'exclude_vmids', emptyText: '100,101,102' },
                            { xtype: 'textfield', fieldLabel: 'Etiketler', name: 'exclude_tags', emptyText: 'kritik,dc,pinned' },
                            { xtype: 'textfield', fieldLabel: 'Nodelar', name: 'exclude_nodes', emptyText: 'VMP1,backup-node' },
                            { xtype: 'textfield', fieldLabel: 'VM Isimleri', name: 'exclude_names', emptyText: 'test-*,dev-*' }
                        ]},
                        { xtype: 'fieldset', title: 'Affinity Kurallari', collapsible: true, collapsed: true, defaults: { anchor: '100%', labelWidth: 150 }, items: [
                            { xtype: 'textarea', fieldLabel: 'Affinity Gruplar', name: 'affinity_groups', height: 50, emptyText: 'db1,db2:VMP1 (ayni nodeda)' },
                            { xtype: 'textarea', fieldLabel: 'Anti-Affinity', name: 'anti_affinity', height: 50, emptyText: 'web1,web2 (farkli nodelarda)' }
                        ]},
                        { xtype: 'fieldset', title: 'Bildirimler', collapsible: true, collapsed: true, defaults: { anchor: '100%', labelWidth: 150 }, items: [
                            { xtype: 'checkbox', fieldLabel: 'Email Bildirim', name: 'notify_email', checked: false },
                            { xtype: 'textfield', fieldLabel: 'Email Adresi', name: 'notify_email_address', emptyText: 'admin@example.com' },
                            { xtype: 'checkbox', fieldLabel: 'Webhook Aktif', name: 'notify_webhook', checked: false },
                            { xtype: 'textfield', fieldLabel: 'Webhook URL', name: 'notify_webhook_url', emptyText: 'https://hooks.slack.com/...' }
                        ]}
                    ],
                    buttons: [
                        { text: 'Dashboard', iconCls: 'fa fa-chart-pie', handler: function() { openDashboard(); } },
                        '->',
                        { text: 'Sifirla', iconCls: 'fa fa-undo', handler: function() { this.up('form').reset(); } },
                        { text: 'Kaydet', iconCls: 'fa fa-save', handler: function() {
                            var form = this.up('form');
                            if (form.isValid()) {
                                Ext.Ajax.request({
                                    url: API_URL + '/config',
                                    method: 'POST',
                                    jsonData: form.getValues(),
                                    success: function() { Ext.Msg.alert('OK', 'Ayarlar kaydedildi'); },
                                    failure: function() { Ext.Msg.alert('Hata', 'Kaydedilemedi'); }
                                });
                            }
                        }}
                    ],
                    listeners: {
                        afterrender: function(form) {
                            Ext.Ajax.request({
                                url: API_URL + '/config',
                                success: function(r) {
                                    try { form.setValues(Ext.decode(r.responseText)); } catch(e) {}
                                }
                            });
                        }
                    }
                }]
            });
            win.show();
        }
    }

    function openExternal() {
        var menu = document.getElementById('proxlb-menu');
        if (menu) menu.classList.remove('show');
        window.open(DASHBOARD_URL, '_blank');
    }

    // Expose functions globally
    window.ProxLB = {
        openDashboard: openDashboard,
        openSettings: openSettings,
        openExternal: openExternal
    };

    // Initialize when DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
