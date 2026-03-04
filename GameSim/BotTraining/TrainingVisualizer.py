import socket
import threading
import time
from collections import deque

from flask import Flask, jsonify


_DASHBOARD_HTML = """<!DOCTYPE html>
<html>
<head>
<title>RL Training Dashboard</title>
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: #1e1e2e; color: #cdd6f4; font-family: monospace; padding: 10px; }
h1 { text-align: center; padding: 10px 0 6px; color: #cba6f7; font-size: 1.3em; }
.grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
.chart-box { background: #181825; border-radius: 8px; padding: 8px; }
.chart-title { color: #89b4fa; font-size: 0.85em; margin-bottom: 4px; font-weight: bold; }
#status { text-align: center; color: #6c7086; font-size: 0.75em; padding: 4px 0 8px; }
.stats-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; padding: 4px 0; }
.stat { background: #313244; border-radius: 4px; padding: 8px 10px; }
.stat-label { color: #6c7086; font-size: 0.7em; text-transform: uppercase; letter-spacing: 0.05em; }
.stat-value { color: #a6e3a1; font-size: 1.05em; font-weight: bold; margin-top: 2px; }
@media (max-width: 1000px) { .grid { grid-template-columns: 1fr 1fr; } }
@media (max-width: 600px) { .grid { grid-template-columns: 1fr; } }
</style>
</head>
<body>
<h1>RL Training Dashboard</h1>
<div id="status">Connecting...</div>
<div class="grid">
  <div class="chart-box"><div class="chart-title">Training Losses</div><div id="c1"></div></div>
  <div class="chart-box"><div class="chart-title">Total Loss</div><div id="c2"></div></div>
  <div class="chart-box"><div class="chart-title">Episode Reward</div><div id="c3"></div></div>
  <div class="chart-box"><div class="chart-title">Combat Win Rate</div><div id="c4"></div></div>
  <div class="chart-box"><div class="chart-title">Health Lost / Combat</div><div id="c5"></div></div>
  <div class="chart-box"><div class="chart-title">Training Health</div><div id="c6"></div></div>
  <div class="chart-box"><div class="chart-title">Hyperparameters</div><div id="c7"></div></div>
  <div class="chart-box">
    <div class="chart-title">Summary</div>
    <div class="stats-grid">
      <div class="stat"><div class="stat-label">Episodes</div><div class="stat-value" id="s-ep">-</div></div>
      <div class="stat"><div class="stat-label">Total Combats</div><div class="stat-value" id="s-cb">-</div></div>
      <div class="stat"><div class="stat-label">Win Rate (100)</div><div class="stat-value" id="s-wr100">-</div></div>
      <div class="stat"><div class="stat-label">Win Rate (1000)</div><div class="stat-value" id="s-wr1000">-</div></div>
      <div class="stat"><div class="stat-label">Best Reward</div><div class="stat-value" id="s-br">-</div></div>
      <div class="stat"><div class="stat-label">Learn Rate</div><div class="stat-value" id="s-lr">-</div></div>
      <div class="stat"><div class="stat-label">Entropy Coef</div><div class="stat-value" id="s-ent">-</div></div>
      <div class="stat"><div class="stat-label">Learn Steps</div><div class="stat-value" id="s-ls">-</div></div>
    </div>
  </div>
</div>
<script>
const BG = '#181825', PAPER = '#181825', FONT = '#cdd6f4', GRID = '#313244';
const C = {
  blue:'#89b4fa', green:'#a6e3a1', red:'#f38ba8',
  yellow:'#f9e2af', mauve:'#cba6f7', peach:'#fab387',
  teal:'#94e2d5', sky:'#89dceb'
};
const BASE_LAYOUT = {
  paper_bgcolor: PAPER, plot_bgcolor: BG,
  font: {color: FONT, size: 10},
  margin: {l: 42, r: 10, t: 8, b: 28},
  height: 195,
  showlegend: true,
  legend: {bgcolor: 'rgba(0,0,0,0)', font: {size: 8}, orientation: 'h', y: -0.18},
  xaxis: {gridcolor: GRID, zerolinecolor: '#45475a'},
  yaxis: {gridcolor: GRID, zerolinecolor: '#45475a'},
};
function layout(extra) {
  return Object.assign({}, BASE_LAYOUT, extra,
    extra && extra.xaxis ? {xaxis: Object.assign({}, BASE_LAYOUT.xaxis, extra.xaxis)} : {},
    extra && extra.yaxis ? {yaxis: Object.assign({}, BASE_LAYOUT.yaxis, extra.yaxis)} : {}
  );
}

const inited = {};
function plot(id, traces, lay) {
  if (!inited[id]) { Plotly.newPlot(id, traces, lay, {responsive:true, displayModeBar:false}); inited[id]=true; }
  else Plotly.react(id, traces, lay);
}

let lastUpdate = null;

function fetchAndUpdate() {
  fetch('/api/metrics').then(r => r.json()).then(d => {
    lastUpdate = Date.now();
    const t = d.train, c = d.combat, s = d.summary;

    // Chart 1: Training Losses
    plot('c1', [
      {x:t.steps, y:t.policy_loss, name:'Policy', line:{color:C.blue,   width:1}, opacity:0.7},
      {x:t.steps, y:t.value_loss,  name:'Value',  line:{color:C.green,  width:1}, opacity:0.7},
      {x:t.steps, y:t.entropy,     name:'Entropy',line:{color:C.yellow, width:1}, opacity:0.7},
      {x:t.steps, y:t.policy_loss_r50, name:'Pol r50', line:{color:C.mauve, width:2}},
    ], layout());

    // Chart 2: Total Loss
    plot('c2', [
      {x:t.steps, y:t.total_loss,     name:'Total', line:{color:C.red,   width:1}, opacity:0.6},
      {x:t.steps, y:t.total_loss_r50, name:'r50',   line:{color:C.peach, width:2}},
    ], layout());

    // Chart 3: Episode Reward
    plot('c3', [
      {x:t.steps, y:t.avg_reward,       name:'Reward', line:{color:C.green, width:1}, opacity:0.5},
      {x:t.steps, y:t.avg_reward_r100,  name:'r100',   line:{color:C.teal,  width:2}},
      {x:t.steps, y:t.avg_reward_r1000, name:'r1000',  line:{color:C.sky,   width:2}},
    ], layout());

    // Chart 4: Combat Win Rate
    plot('c4', [
      {x:c.numbers, y:c.win_rate_r100,  name:'WR r100',  line:{color:C.green, width:2}},
      {x:c.numbers, y:c.win_rate_r1000, name:'WR r1000', line:{color:C.teal,  width:2}},
    ], layout({yaxis: {range:[0,1], gridcolor:GRID}}));

    // Chart 5: Health Lost / Combat
    plot('c5', [
      {x:c.numbers, y:c.health_lost,      name:'HP Lost', line:{color:C.red,   width:1}, opacity:0.4},
      {x:c.numbers, y:c.health_lost_r100, name:'r100',    line:{color:C.peach, width:2}},
    ], layout());

    // Chart 6: Training Health
    plot('c6', [
      {x:t.steps, y:t.clip_fraction, name:'Clip Frac', line:{color:C.yellow, width:1}},
      {x:t.steps, y:t.advantage_std, name:'Adv Std',   line:{color:C.mauve,  width:1}},
      {x:t.steps, y:t.grad_norm,     name:'Grad Norm', line:{color:C.peach,  width:1}},
    ], layout());

    // Chart 7: Hyperparameters (dual y-axis)
    plot('c7', [
      {x:t.steps, y:t.learn_rate,   name:'LR',      yaxis:'y',  line:{color:C.blue,  width:2}},
      {x:t.steps, y:t.entropy_coef, name:'Ent Coef',yaxis:'y2', line:{color:C.mauve, width:2}},
    ], Object.assign({}, BASE_LAYOUT, {
      yaxis:  {title:{text:'LR',  font:{size:9}}, gridcolor:GRID, color:C.blue,  tickfont:{size:8}},
      yaxis2: {title:{text:'Ent', font:{size:9}}, overlaying:'y', side:'right', color:C.mauve, tickfont:{size:8}, gridcolor:'rgba(0,0,0,0)'},
    }));

    // Stats panel
    document.getElementById('s-ep').textContent    = s.total_episodes;
    document.getElementById('s-cb').textContent    = s.total_combats;
    document.getElementById('s-wr100').textContent = (s.win_rate_100  * 100).toFixed(1) + '%';
    document.getElementById('s-wr1000').textContent= (s.win_rate_1000 * 100).toFixed(1) + '%';
    document.getElementById('s-br').textContent    = s.best_reward.toFixed(3);
    document.getElementById('s-lr').textContent    = s.current_lr.toExponential(2);
    document.getElementById('s-ent').textContent   = s.current_entropy_coef.toExponential(2);
    document.getElementById('s-ls').textContent    = s.learn_steps;
  }).catch(e => console.error('Fetch error:', e));
}

setInterval(fetchAndUpdate, 2000);
fetchAndUpdate();

setInterval(() => {
  if (lastUpdate) {
    const sec = Math.floor((Date.now() - lastUpdate) / 1000);
    document.getElementById('status').textContent = 'Last updated: ' + sec + 's ago';
  }
}, 1000);
</script>
</body>
</html>"""


class TrainingVisualizer:
    def __init__(self, port=5000, max_history=10000):
        self._port = port
        self._lock = threading.Lock()
        self._train_steps = deque(maxlen=max_history)
        self._combats = deque(maxlen=max_history)
        self._episodes = deque(maxlen=max_history)
        self._combat_count = 0
        self._app = Flask(__name__)
        self._setup_routes()

    def start(self):
        port = self._port
        while True:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.bind(('', port))
                s.close()
                break
            except OSError:
                s.close()
                print(f"[Visualizer] Port {port} in use, trying {port + 1}")
                port += 1
        self._port = port
        t = threading.Thread(target=self._run_flask, daemon=True)
        t.start()
        time.sleep(0.5)
        print(f"[Visualizer] Dashboard: http://localhost:{self._port}")

    def _run_flask(self):
        import logging
        logging.getLogger('werkzeug').setLevel(logging.ERROR)
        self._app.run(host='0.0.0.0', port=self._port, debug=False, use_reloader=False)

    def log_training_step(self, policy_loss, value_loss, entropy, clip_fraction,
                          advantage_std, grad_norm, total_loss, avg_reward,
                          learn_rate, entropy_coef, learn_step):
        with self._lock:
            self._train_steps.append({
                'policy_loss':   policy_loss,
                'value_loss':    value_loss,
                'entropy':       entropy,
                'clip_fraction': clip_fraction,
                'advantage_std': advantage_std,
                'grad_norm':     grad_norm,
                'total_loss':    total_loss,
                'avg_reward':    avg_reward,
                'learn_rate':    learn_rate,
                'entropy_coef':  entropy_coef,
                'learn_step':    learn_step,
            })

    def log_combat(self, win: bool, health_lost: float, turns: int,
                   cards_played: int, episode: int):
        with self._lock:
            self._combat_count += 1
            self._combats.append({
                'number':       self._combat_count,
                'win':          int(win),
                'health_lost':  health_lost,
                'turns':        turns,
                'cards_played': cards_played,
                'episode':      episode,
            })

    def log_episode(self, combats: int, combats_won: int, episode: int):
        with self._lock:
            self._episodes.append({
                'combats':      combats,
                'combats_won':  combats_won,
                'episode':      episode,
            })

    @staticmethod
    def _rolling_avg(series, window):
        result = []
        total = 0.0
        for i, v in enumerate(series):
            total += v
            if i >= window:
                total -= series[i - window]
            count = min(i + 1, window)
            result.append(total / count)
        return result

    def _setup_routes(self):
        @self._app.route('/')
        def index():
            return _DASHBOARD_HTML

        @self._app.route('/api/metrics')
        def metrics():
            with self._lock:
                train_steps = list(self._train_steps)
                combats     = list(self._combats)
                episodes    = list(self._episodes)

            steps         = [s['learn_step']    for s in train_steps]
            policy_loss   = [s['policy_loss']   for s in train_steps]
            value_loss    = [s['value_loss']     for s in train_steps]
            entropy       = [s['entropy']        for s in train_steps]
            total_loss    = [s['total_loss']     for s in train_steps]
            clip_fraction = [s['clip_fraction']  for s in train_steps]
            advantage_std = [s['advantage_std']  for s in train_steps]
            grad_norm     = [s['grad_norm']      for s in train_steps]
            avg_reward    = [s['avg_reward']     for s in train_steps]
            learn_rate    = [s['learn_rate']     for s in train_steps]
            entropy_coef  = [s['entropy_coef']   for s in train_steps]

            combat_numbers = [c['number']       for c in combats]
            wins           = [c['win']          for c in combats]
            health_lost    = [c['health_lost']  for c in combats]
            turns          = [c['turns']        for c in combats]
            cards_played   = [c['cards_played'] for c in combats]

            recent_100_wins   = wins[-100:]  if wins else []
            recent_1000_wins  = wins[-1000:] if wins else []

            return jsonify({
                'train': {
                    'steps':             steps,
                    'policy_loss':       policy_loss,
                    'value_loss':        value_loss,
                    'entropy':           entropy,
                    'total_loss':        total_loss,
                    'clip_fraction':     clip_fraction,
                    'advantage_std':     advantage_std,
                    'grad_norm':         grad_norm,
                    'avg_reward':        avg_reward,
                    'learn_rate':        learn_rate,
                    'entropy_coef':      entropy_coef,
                    'policy_loss_r50':   self._rolling_avg(policy_loss, 50),
                    'total_loss_r50':    self._rolling_avg(total_loss, 50),
                    'avg_reward_r100':   self._rolling_avg(avg_reward, 100),
                    'avg_reward_r1000':  self._rolling_avg(avg_reward, 1000),
                },
                'combat': {
                    'numbers':           combat_numbers,
                    'wins':              wins,
                    'health_lost':       health_lost,
                    'turns':             turns,
                    'cards_played':      cards_played,
                    'win_rate_r100':     self._rolling_avg(wins, 100),
                    'win_rate_r1000':    self._rolling_avg(wins, 1000),
                    'health_lost_r100':  self._rolling_avg(health_lost, 100),
                    'turns_r100':        self._rolling_avg(turns, 100),
                },
                'summary': {
                    'total_episodes':       len(episodes),
                    'total_combats':        len(combats),
                    'win_rate_100':         sum(recent_100_wins)  / len(recent_100_wins)  if recent_100_wins  else 0.0,
                    'win_rate_1000':        sum(recent_1000_wins) / len(recent_1000_wins) if recent_1000_wins else 0.0,
                    'best_reward':          max(avg_reward) if avg_reward else 0.0,
                    'current_lr':           learn_rate[-1]   if learn_rate   else 0.0,
                    'current_entropy_coef': entropy_coef[-1] if entropy_coef else 0.0,
                    'learn_steps':          len(train_steps),
                },
            })
