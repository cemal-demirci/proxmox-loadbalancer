// Proxmox Load Balancer UI - v3.0
// Cemal Demirci | github.com/cemal-demirci

(function() {
    var DASHBOARD = "http://" + window.location.hostname + ":5000";
    var buttonAdded = false;
    
    function addButton() {
        if (buttonAdded) return;
        if (typeof Ext === "undefined") {
            setTimeout(addButton, 500);
            return;
        }
        
        Ext.onReady(function() {
            setTimeout(function() {
                // Find main toolbar
                var viewports = Ext.ComponentQuery.query("viewport");
                if (!viewports.length) {
                    console.log("ProxLB: No viewport found, retrying...");
                    setTimeout(addButton, 1000);
                    return;
                }
                
                var vp = viewports[0];
                var toolbars = vp.query("toolbar[dock=top]");
                
                for (var i = 0; i < toolbars.length; i++) {
                    var tb = toolbars[i];
                    if (tb.items && tb.items.length > 3) {
                        // Check if button already exists
                        var exists = false;
                        tb.items.each(function(item) {
                            if (item.text === "Load Balancer") exists = true;
                        });
                        
                        if (exists) {
                            buttonAdded = true;
                            return;
                        }
                        
                        // Find position after Documentation
                        var insertIdx = 2;
                        tb.items.each(function(item, idx) {
                            if (item.text && item.text.indexOf("Documentation") > -1) {
                                insertIdx = idx + 1;
                            }
                        });
                        
                        // Create button
                        var btn = Ext.create("Ext.button.Button", {
                            text: "Load Balancer",
                            iconCls: "fa fa-balance-scale",
                            handler: function() {
                                openDashboard();
                            }
                        });
                        
                        tb.insert(insertIdx, btn);
                        buttonAdded = true;
                        console.log("ProxLB: Button added to toolbar");
                        return;
                    }
                }
                
                // Fallback: floating button
                if (!buttonAdded) {
                    createFloatingButton();
                }
            }, 3000);
        });
    }
    
    function createFloatingButton() {
        if (document.getElementById("proxlb-float-btn")) return;
        
        var btn = document.createElement("div");
        btn.id = "proxlb-float-btn";
        btn.innerHTML = "LB";
        btn.title = "Load Balancer Dashboard";
        btn.style.cssText = "position:fixed;bottom:20px;right:20px;width:50px;height:50px;background:#2196F3;color:white;border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer;font-weight:bold;font-size:14px;box-shadow:0 4px 8px rgba(0,0,0,0.3);z-index:99999;";
        btn.onclick = openDashboard;
        document.body.appendChild(btn);
        buttonAdded = true;
        console.log("ProxLB: Floating button added");
    }
    
    function openDashboard() {
        var win = window.open("", "proxlb_dashboard", "width=1400,height=900");
        if (win.location.href === "about:blank" || !win.document.body.innerHTML) {
            win.location.href = DASHBOARD;
        } else {
            win.focus();
        }
    }
    
    // Start
    if (document.readyState === "complete") {
        addButton();
    } else {
        window.addEventListener("load", addButton);
    }
})();
