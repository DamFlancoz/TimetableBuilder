$(function () {
    /**
     * @fileoverview Defines functions to handle tabs.
     */

    /**
     * Adds a tab to your choice of $tabPanel with content and header provided.
     * @param {jQuery Object} $tabPanels JQuery object containing tabs.
     * @param {string} header Name displayed in tab.
     * @param {content} content Html content for tab body.
     * @param {function=} callback Optional callback function. No arguments.
     *
     * @global
     */
    function addTab($tabPanels, header, content, callback = undefined) {
        // create
        var $tab = $("<li></li>")
            .text(header)
            .attr({
                rel: header.replace(" ", "-")
            })
            .on("click", toggleTab);

        // add close button
        $tab.append(
            $("<span>")
                .addClass("close")
                .on("click", closeTab)
        );

        // add tab
        $tabPanels.find(".tabs").append($tab);

        var $panel = $("<div></div>")
            .addClass("panel")
            .attr({
                id: header.replace(" ", "-")
            })
            .html(content);

        //create and add panel
        $tabPanels.append($panel);

        //select this tab
        $tab.click();

        callback && callback();
    }

    /**
     * Changes to 'this' tab. Used to change to clicked tab.
     * @global
     */
    function toggleTab() {
        var $panel = $(this).closest(".tab-panels");

        $panel.find(".tabs li.active").removeClass("active");
        $(this).addClass("active");

        //figure out which panel to show
        var panelToShow = $(this).attr("rel");

        //hide current panel if exists (might not at start)
        var $activePanel = $panel.find(".panel.active");

        if ($activePanel[0]) {
            $activePanel.hide(0, showNextPanel);
        } else {
            showNextPanel();
        }

        //show next panel
        function showNextPanel() {
            $(this).removeClass("active");

            $("#" + panelToShow).show(0, function () {
                $(this).addClass("active");
            });
        }
    }

    /**
     * Close current 'this' tab.
     * @global
     */
    function closeTab(callback = undefined) {
        var $tab = $(this).closest("li");

        // show another tab if tab was active
        if ($tab.hasClass("active")) {
            if ($tab.next()[0]) {
                $tab.next().trigger("click");
            } else {
                $tab.prev().trigger("click");
            }
        }

        $("#" + $tab.attr("rel")).remove();
        $tab.remove();

        typeof callback === "function" && callback();
    }

    // Add all functions to global scope
    window.addTab = addTab;
    window.toggleTab = toggleTab;
    window.closeTab = closeTab;

});
