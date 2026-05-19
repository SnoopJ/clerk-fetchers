browser.runtime.onInstalled.addListener(() => {
  browser.action.setBadgeText({
    text: "OFF", //Extension is off by default when installed
  });
});

browser.action.onClicked.addListener(async (tab) => {
    // Retrieve the action badge to check if the extension is 'ON' or 'OFF'
    const prevState = await browser.action.getBadgeText({ tabId: tab.id });
    
    // Next state will always be the opposite
    const nextState = prevState === 'ON' ? 'OFF' : 'ON';
    
    // Set the action badge to the next state
    await browser.action.setBadgeText({
      tabId: tab.id,
      text: nextState,
    });

    if (nextState === "ON") {
      let currentTabURL;
      try {
        currentTabURL = tab.url;
        currentTabTitle = tab.title;
        if (!currentTabURL) {
          throw new Error("Invalid tab! It might be empty or undefined.");
        }
      } 
      catch (error) {
        console.error("Invalid tab! It might be empty or undefined.", error);
        return;
         }
      console.log(currentTabURL);
      // All the checks go in here
      if (currentTabURL.includes(".civicclerk.com/")){
        await browser.action.setPopup({ tabId: tab.id, popup: "civicclerk.html" });
        await browser.action.openPopup();
        } 
      else if (currentTabURL.includes(".legistar.com")){
        await browser.action.setPopup({ tabId: tab.id, popup: "legistar.html" });
        await browser.action.openPopup();
        } 
      else if (currentTabURL.includes(".granicus.com")){
        await browser.action.setPopup({ tabId: tab.id, popup: "granicus.html" });
        await browser.action.openPopup();
        }
      else if (currentTabURL.includes(".escribemeetings.com")){
        await browser.action.setPopup({ tabId: tab.id, popup: "escribe.html" });
        await browser.action.openPopup();
        }
      else if (currentTabURL.includes(".primegov.com")){
        await browser.action.setPopup({ tabId: tab.id, popup: "primegov.html" });
        await browser.action.openPopup();
        }
      else if (currentTabURL.endsWith("/AgendaCenter")){
        //NOTE: AgendaCenter is more prevalent than some of those that come before it in this list, 
        // but some pages false-flag agendacenter when they're actually embeds from a previous option, 
        // so we should NOT move this up the list.
        await browser.action.setPopup({ tabId: tab.id, popup: "agendacenter.html" });
        await browser.action.openPopup();
        }
      else if (currentTabURL.includes(".iqm2.com")){
        await browser.action.setPopup({ tabId: tab.id, popup: "iqm2.html" });
        await browser.action.openPopup();
        }
      else if (currentTabURL.includes("onbase") || currentTabTitle.includes("OnBase Agenda Online")){
        await browser.action.setPopup({ tabId: tab.id, popup: "onbase.html" });
        await browser.action.openPopup();
        } // This is where Municode falls by prevalence but I've deprioritized for speed
      else if (currentTabURL.includes(".eboardsolutions.com")){
        await browser.action.setPopup({ tabId: tab.id, popup: "eboard.html" });
        await browser.action.openPopup();
        }
      else if (currentTabTitle.includes("Laserfiche")){
        await browser.action.setPopup({ tabId: tab.id, popup: "laserfiche.html" });
        await browser.action.openPopup();
        }  
      //else if (source includes "Aha change 20170911"): municode 
        // Comment originating from a dependency but their code uses such clear language 
        // that nothing else feels specific to them
      
      //else if (there's an Archive link): ask the user to click it and run this again
        else {
          await browser.action.setPopup({ tabId: tab.id, popup: "hello.html" });
          await browser.action.openPopup();
        }
      };
});