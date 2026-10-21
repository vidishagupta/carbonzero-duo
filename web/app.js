/**
 * CarbonZero Duo Frontend Client:
 * Handles real-time telemetry updates, interactive simulator calculations,
 * and the GitLab Duo Autonomous Flow step-by-step execution simulation.
 */

document.addEventListener('DOMContentLoaded', () => {
  initRegions();
  initSimulator();
  initMcpTools();
  initFlowSimulator();
});

// 1. Regions Telemetry
async function initRegions() {
  const grid = document.getElementById('regionsGrid');
  const btnRefresh = document.getElementById('btnRefreshRegions');

  async function loadRegions() {
    try {
      const res = await fetch('/api/regions');
      const data = await res.json();
      renderRegions(data.regions);
    } catch (err) {
      grid.innerHTML = `<div class="error">Failed to fetch telemetry: ${err.message}</div>`;
    }
  }

  btnRefresh.addEventListener('click', () => {
    grid.innerHTML = `<div class="loading-spinner">Refreshing Google Cloud telemetry...</div>`;
    loadRegions();
  });

  loadRegions();
}

function renderRegions(regions) {
  const grid = document.getElementById('regionsGrid');
  grid.innerHTML = '';

  regions.forEach((reg, idx) => {
    const isCleanest = idx === 0;
    const card = document.createElement('div');
    card.className = `region-card ${isCleanest ? 'recommended' : ''}`;

    const gradeClass = reg.clean_rank === 'A+' ? 'grade-A-plus' : (reg.clean_rank === 'A' ? 'grade-A' : (reg.clean_rank === 'B' ? 'grade-B' : 'grade-C'));

    card.innerHTML = `
      <div class="card-top">
        <div>
          <div class="region-code">${reg.region} ${isCleanest ? '★' : ''}</div>
          <div class="region-loc">${reg.location}</div>
        </div>
        <div class="grade-badge ${gradeClass}">${reg.clean_rank}</div>
      </div>
      <div>
        <span class="intensity-metric">${reg.carbon_intensity_gco2_kwh}</span>
        <span class="intensity-unit">gCO₂eq/kWh</span>
      </div>
      <div class="cfe-meter-track">
        <div class="cfe-meter-fill" style="width: ${reg.cfe_percentage}%;"></div>
      </div>
      <div class="cfe-label">
        <span>Carbon-Free Energy:</span>
        <strong>${reg.cfe_percentage}% CFE</strong>
      </div>
    `;
    grid.appendChild(card);
  });
}

// 2. Interactive Pipeline Carbon Savings Simulator
function initSimulator() {
  const inputDuration = document.getElementById('inputDuration');
  const inputVcpus = document.getElementById('inputVcpus');
  const inputRam = document.getElementById('inputRam');
  const selectRegion = document.getElementById('selectCurrentRegion');

  const valDuration = document.getElementById('valDuration');
  const valVcpus = document.getElementById('valVcpus');
  const valRam = document.getElementById('valRam');

  async function updateSimulation() {
    const duration = parseFloat(inputDuration.value);
    const vcpus = parseInt(inputVcpus.value);
    const ram = parseInt(inputRam.value);
    const region = selectRegion.value;

    valDuration.textContent = duration;
    valVcpus.textContent = vcpus;
    valRam.textContent = ram;

    try {
      const res = await fetch('/api/calculate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ duration_minutes: duration, vcpus, ram_gb: ram, region })
      });
      const data = await res.json();
      renderSimulationResults(data);
    } catch (err) {
      console.error('Calculation error:', err);
    }
  }

  [inputDuration, inputVcpus, inputRam, selectRegion].forEach(el => {
    el.addEventListener('input', updateSimulation);
  });

  updateSimulation();
}

function renderSimulationResults(data) {
  document.getElementById('simSavingsPercent').textContent = `-${data.potential_savings_percentage}%`;
  document.getElementById('simCurrentLabel').textContent = data.current_region;
  document.getElementById('simCleanLabel').textContent = data.cleanest_region_alternative;

  document.getElementById('valCurrentEmissions').textContent = `${data.carbon_emitted_gco2} gCO₂`;
  document.getElementById('valCleanEmissions').textContent = `${data.cleanest_region_emissions_gco2} gCO₂`;

  // Bars scale
  const maxEmissions = Math.max(data.carbon_emitted_gco2, 0.001);
  const cleanPercent = Math.max(10, Math.round((data.cleanest_region_emissions_gco2 / maxEmissions) * 100));
  document.getElementById('barCurrent').style.width = '100%';
  document.getElementById('barOptimized').style.width = `${cleanPercent}%`;

  document.getElementById('metricEnergy').textContent = `${data.energy_consumed_kwh} kWh`;
  document.getElementById('metricCarKm').textContent = `${data.equivalent_car_meters_driven} m`;
  
  // 50 runs/day over 1 year
  const annualKg = ((data.potential_savings_gco2 * 50 * 365) / 1000).toFixed(1);
  document.getElementById('metricAnnual').textContent = `${annualKg} kg/yr`;
}

// 3. MCP Tools List
async function initMcpTools() {
  const container = document.getElementById('mcpToolsGrid');
  try {
    const res = await fetch('/api/mcp-tools');
    const data = await res.json();
    container.innerHTML = '';
    data.tools.forEach(tool => {
      const card = document.createElement('div');
      card.className = 'mcp-card';
      card.innerHTML = `
        <div class="mcp-name">🔧 ${tool.name}</div>
        <div class="mcp-desc">${tool.description}</div>
      `;
      container.appendChild(card);
    });
  } catch (err) {
    container.innerHTML = `<p class="error">Failed to load MCP tools</p>`;
  }
}

// 4. Autonomous Flow Simulation
function initFlowSimulator() {
  const btnTrigger = document.getElementById('btnTriggerFlow');
  const section = document.getElementById('flowSimulationSection');
  const btnClose = document.getElementById('btnCloseFlow');
  const timeline = document.getElementById('flowTimeline');
  const codeBox = document.getElementById('codePatchContent');
  const gbomBox = document.getElementById('gbomMarkdownContent');

  btnClose.addEventListener('click', () => {
    section.classList.add('hidden');
  });

  btnTrigger.addEventListener('click', async () => {
    section.classList.remove('hidden');
    section.scrollIntoView({ behavior: 'smooth' });

    timeline.innerHTML = '';
    codeBox.textContent = 'Initiating GitLab Duo Agent Platform event trigger...';
    gbomBox.innerHTML = '<p class="loading-spinner">Waiting for agent orchestration...</p>';

    try {
      const res = await fetch('/api/simulate-duo-flow', { method: 'POST' });
      const data = await res.json();

      // Render timeline steps sequentially
      for (let i = 0; i < data.stages_executed.length; i++) {
        const stage = data.stages_executed[i];
        const stepEl = document.createElement('div');
        stepEl.className = 'timeline-step active';
        stepEl.innerHTML = `
          <div class="timeline-step-title">${stage.stage}</div>
          <div class="timeline-step-desc">${stage.action || stage.agent || stage.target}</div>
        `;
        timeline.appendChild(stepEl);

        await new Promise(r => setTimeout(r, 450));
        stepEl.classList.remove('active');
        stepEl.classList.add('completed');
      }

      // Display the generated Git patch diff
      codeBox.textContent = `--- a/k8s/deployment.yaml
+++ b/k8s/deployment.yaml
@@ -14,8 +14,8 @@
         resources:
           requests:
-            cpu: "2000m"
-            memory: "4Gi"
+            cpu: "350m"
+            memory: "1Gi"
           limits:
-            cpu: "4000m"
-            memory: "8Gi"
+            cpu: "700m"
+            memory: "2Gi"`;

      // Render markdown
      renderGbomPreview(data.gbom_markdown, gbomBox);

    } catch (err) {
      codeBox.textContent = `Simulation error: ${err.message}`;
    }
  });
}

function renderGbomPreview(markdown, container) {
  // Convert basic markdown to formatted HTML
  let html = markdown
    .replace(/^### (.*$)/gim, '<h3>$1</h3>')
    .replace(/^## (.*$)/gim, '<h2>$1</h2>')
    .replace(/^> (.*$)/gim, '<blockquote style="border-left: 3px solid #00E599; padding-left: 10px; color: #94A3B8;">$1</blockquote>')
    .replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>')
    .replace(/`(.*?)`/gim, '<code style="background: rgba(255,255,255,0.08); padding: 2px 6px; border-radius: 4px; font-family: monospace;">$1</code>')
    .replace(/\n\n/gim, '<br><br>');

  container.innerHTML = html;
}
