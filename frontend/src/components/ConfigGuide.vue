<template>
  <BCard no-body>
    <div class="card-header"><IBiTerminal class="me-2" />Configuration Guide</div>
    <div class="card-body">
      <BTabs pills small content-class="mt-3">
        <!-- Docker -->
        <BTab title="Docker (StayRTR)" active>
          <div class="code-box">
            <button class="copy-btn" @click="copy(dockerCode)">Copy</button>
            <pre class="m-0">{{ dockerCode }}</pre>
          </div>
          <div class="mt-2 text-muted small">
            Replace <code>{name}</code> with:
            <span class="font-monospace text-info">all, min_2, min_3, min_5</span>.
          </div>
        </BTab>

        <!-- Bird -->
        <BTab title="BIRD (Direct)">
          <div class="code-box">
            <button class="copy-btn" @click="copy(birdCode)">Copy</button>
            <pre class="m-0">{{ birdCode }}</pre>
          </div>
        </BTab>

        <!-- Join -->
        <BTab title="Provide Data">
          <div class="mb-4">
            <div class="text-h5 mb-2">Method 1: Polling</div>
            <div class="text-muted mb-1 small">Open up API access and tell us your FlapAlerted URL.</div>
            <div class="text-muted mb-1 small">
              Check if <code>your-endpoint.domain/flaps/active/compact</code> is available.
            </div>
          </div>
          <div>
            <div class="text-h5 mb-2">Method 2: Webhook</div>
            <div class="mb-1 text-muted small">Contact us to get your Instance ID, then configure your FlapAlerted to setup webhooks.</div>
            <div class="code-box">
              <button class="copy-btn" @click="copy(webhookCode)">Copy</button>
              <pre class="m-0">{{ webhookCode }}</pre>
            </div>
          </div>
        </BTab>
      </BTabs>
    </div>
  </BCard>
</template>

<script setup lang="ts">
import { BCard, BTabs, BTab } from 'bootstrap-vue-next'

const dockerCode = `services:
  stayrtr:
    image: rpki/stayrtr:latest
    ports: ["8082:8282"]
    command: >
      -cache https://flap-data.nia.dn42/{name}.json`

const birdCode = `protocol rpki roa_dn42_flap {
    roa4 { table roa_dn42_flap_4; };
    roa6 { table roa_dn42_flap_6; };
    remote "rpki.nia.dn42" port 8083;
    retry keep 120;
    refresh keep 300;
    expire keep 600;
}`

const webhookCode = `# FlapAlerted > 4.1.5 required
-webhookInstanceName "Instance ID"
-webhookUrlStart "https://flap-data.nia.dn42/start"
# for IANA: -webhookUrlStart "https://flap42-data.strexp.net/start"
-webhookUrlEnd "https://flap-data.nia.dn42/end"
# for IANA: -webhookUrlStart "https://flap42-data.strexp.net/end"`

const copy = (txt: string) => navigator.clipboard.writeText(txt)
</script>
