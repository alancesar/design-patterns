import MDXComponents from '@theme-original/MDXComponents';
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

// Makes <Tabs> and <TabItem> available in every MDX page without imports.
// Pattern pages use them for the language tabs of the example section.
export default {
  ...MDXComponents,
  Tabs,
  TabItem,
};
