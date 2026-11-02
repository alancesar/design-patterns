import type {PrismTheme} from 'prism-react-renderer';

// Catppuccin palettes (https://catppuccin.com/palette/), same flavors as alancesar.dev.
type Palette = Record<
  'base' | 'mantle' | 'text' | 'overlay2' | 'mauve' | 'red' | 'peach' | 'yellow' | 'green' | 'teal' | 'sky' | 'blue' | 'lavender' | 'pink',
  string
>;

const latte: Palette = {
  base: '#eff1f5', mantle: '#e6e9ef', text: '#4c4f69', overlay2: '#7c7f93',
  mauve: '#8839ef', red: '#d20f39', peach: '#fe640b', yellow: '#df8e1d', green: '#40a02b',
  teal: '#179299', sky: '#04a5e5', blue: '#1e66f5', lavender: '#7287fd', pink: '#ea76cb',
};

const mocha: Palette = {
  base: '#1e1e2e', mantle: '#181825', text: '#cdd6f4', overlay2: '#9399b2',
  mauve: '#cba6f7', red: '#f38ba8', peach: '#fab387', yellow: '#f9e2af', green: '#a6e3a1',
  teal: '#94e2d5', sky: '#89dceb', blue: '#89b4fa', lavender: '#b4befe', pink: '#f5c2e7',
};

function theme(c: Palette): PrismTheme {
  return {
    plain: {color: c.text, backgroundColor: c.mantle},
    styles: [
      {types: ['comment', 'prolog', 'doctype', 'cdata'], style: {color: c.overlay2, fontStyle: 'italic'}},
      {types: ['punctuation'], style: {color: c.overlay2}},
      {types: ['keyword', 'atrule', 'important', 'selector'], style: {color: c.mauve}},
      {types: ['string', 'char', 'attr-value', 'inserted', 'regex'], style: {color: c.green}},
      {types: ['number', 'boolean', 'constant', 'symbol'], style: {color: c.peach}},
      {types: ['function', 'method'], style: {color: c.blue}},
      {types: ['class-name', 'builtin', 'maybe-class-name', 'namespace'], style: {color: c.yellow}},
      {types: ['tag', 'deleted'], style: {color: c.red}},
      {types: ['attr-name', 'property'], style: {color: c.lavender}},
      {types: ['operator', 'entity', 'url'], style: {color: c.sky}},
      {types: ['variable', 'parameter'], style: {color: c.text}},
      {types: ['annotation', 'decorator'], style: {color: c.pink}},
      {types: ['italic'], style: {fontStyle: 'italic'}},
      {types: ['bold'], style: {fontWeight: 'bold'}},
    ],
  };
}

export const catppuccinLatte = theme(latte);
export const catppuccinMocha = theme(mocha);
