// src/data/datasample.js
export const originalCode = `function hello(name) {
  console.log("Hello, " + name + "!");
}

for (let i = 0; i < 5; i++) {
  hello("User " + i);
}

function sum(a, b) {
  return a + b;
}

console.log("Sum: ", sum(10, 20));
`;

export const modifiedCode = `function hello(name) {
  console.log("Hi, " + name + "!");
}

for (let i = 1; i <= 5; i++) {
  hello("Visitor " + i);
}

function sum(a, b, c = 0) {
  return a + b + c;
}

console.log("Total: ", sum(10, 20, 30));
`;

export const changes = [
  { lineNumber: 1, content: '<template>', isConflict: false },
  { lineNumber: 2, content: '  <div class="container">', isConflict: false },
  { lineNumber: 3, content: '    <h1>Hello from Feature</h1>', isConflict: true, charConflictRanges: [{ start: 11, end: 29 }] },
  { lineNumber: 4, content: '    <p>This is the feature version with some new UI.</p>', isConflict: true },
  { lineNumber: 5, content: '    <button @click="handleClick">Click Feature</button>', isConflict: true },
  { lineNumber: 6, content: '  </div>', isConflict: false },
  { lineNumber: 7, content: '</template>', isConflict: false },
  { lineNumber: 8, content: '', isConflict: false },
  { lineNumber: 9, content: '<script>', isConflict: false },
  { lineNumber:10, content: 'export default {', isConflict: false },
  { lineNumber:11, content: '  name: "MyComponent",', isConflict: false },
  { lineNumber:12, content: '  data() {', isConflict: false },
  { lineNumber:13, content: '    return {', isConflict: false },
  { lineNumber:14, content: '      count: 100,', isConflict: true, charConflictRanges: [{ start: 13, end: 16 }] },
  { lineNumber:15, content: '      message: "Feature branch updated message",', isConflict: true },
  { lineNumber:16, content: '      items: ["Item 1", "Item 2"]', isConflict: true },
  { lineNumber:17, content: '    };', isConflict: false },
  { lineNumber:18, content: '  },', isConflict: false },
  { lineNumber:19, content: '  methods: {', isConflict: false },
  { lineNumber:20, content: '    handleClick() {', isConflict: false },
  { lineNumber:21, content: '      this.count += 10;', isConflict: true, charConflictRanges: [{ start: 23, end: 25 }] },
  { lineNumber:22, content: '    },', isConflict: false },
  { lineNumber:23, content: '    greet() {', isConflict: false },
  { lineNumber:24, content: '      console.log("Hello from Feature Branch!");', isConflict: true },
  { lineNumber:25, content: '    },', isConflict: false },
  { lineNumber:26, content: '    newMethod() {', isConflict: true },
  { lineNumber:27, content: '      console.log("This method is new in feature branch.");', isConflict: true },
  { lineNumber:28, content: '    }', isConflict: true },
  { lineNumber:29, content: '  },', isConflict: false },
  { lineNumber:30, content: '  mounted() {', isConflict: false },
  { lineNumber:31, content: '    this.greet();', isConflict: false },
  { lineNumber:32, content: '    this.newMethod();', isConflict: true },
  { lineNumber:33, content: '  }', isConflict: false },
  { lineNumber:34, content: '};', isConflict: false },
  { lineNumber:35, content: '</script>', isConflict: false },
  { lineNumber:36, content: '', isConflict: false },
  { lineNumber:37, content: '<style scoped>', isConflict: false },
  { lineNumber:38, content: '.container {', isConflict: false },
  { lineNumber:39, content: '  padding: 30px;', isConflict: true, charConflictRanges: [{ start: 10, end: 12 }] },
  { lineNumber:40, content: '  background-color: #fff0f0;', isConflict: true },
  { lineNumber:41, content: '}', isConflict: false },
  { lineNumber:42, content: '', isConflict: false },
  { lineNumber:43, content: 'h1 {', isConflict: false },
  { lineNumber:44, content: '  color: red;', isConflict: true },
  { lineNumber:45, content: '}', isConflict: false },
  { lineNumber:46, content: '', isConflict: false },
  { lineNumber:47, content: 'button {', isConflict: false },
  { lineNumber:48, content: '  background-color: pink;', isConflict: true },
  { lineNumber:49, content: '  border: 2px dashed #999;', isConflict: true },
  { lineNumber:50, content: '}', isConflict: false }
]

export const modified = [
  { lineNumber: 1, content: '<template>', isConflict: false },
  { lineNumber: 2, content: '  <div class="container">', isConflict: false },
  { lineNumber: 3, content: '    <h1>Hello again from Main</h1>', isConflict: true, charConflictRanges: [{ start: 11, end: 35 }] },
  { lineNumber: 4, content: '    <p>This main version now includes new info.</p>', isConflict: true },
  { lineNumber: 5, content: '    <button @click="handleClick">Click Main</button>', isConflict: true },
  { lineNumber: 6, content: '  </div>', isConflict: false },
  { lineNumber: 7, content: '</template>', isConflict: false },
  { lineNumber: 8, content: '', isConflict: false },
  { lineNumber: 9, content: '<script>', isConflict: false },
  { lineNumber:10, content: 'export default {', isConflict: false },
  { lineNumber:11, content: '  name: "MyComponent",', isConflict: false },
  { lineNumber:12, content: '  data() {', isConflict: false },
  { lineNumber:13, content: '    return {', isConflict: false },
  { lineNumber:14, content: '      count: 1,', isConflict: true, charConflictRanges: [{ start: 13, end: 14 }] },
  { lineNumber:15, content: '      message: "Main branch updated",', isConflict: true },
  { lineNumber:16, content: '      items: ["Main A", "Main B"]', isConflict: true },
  { lineNumber:17, content: '    };', isConflict: false },
  { lineNumber:18, content: '  },', isConflict: false },
  { lineNumber:19, content: '  methods: {', isConflict: false },
  { lineNumber:20, content: '    handleClick() {', isConflict: false },
  { lineNumber:21, content: '      this.count += 1;', isConflict: true, charConflictRanges: [{ start: 23, end: 24 }] },
  { lineNumber:22, content: '    },', isConflict: false },
  { lineNumber:23, content: '    greet() {', isConflict: false },
  { lineNumber:24, content: '      console.log("Main says hello again!");', isConflict: true },
  { lineNumber:25, content: '    },', isConflict: false },
  { lineNumber:26, content: '    logCount() {', isConflict: true },
  { lineNumber:27, content: '      console.log("Count is", this.count);', isConflict: true },
  { lineNumber:28, content: '    }', isConflict: true },
  { lineNumber:29, content: '  },', isConflict: false },
  { lineNumber:30, content: '  mounted() {', isConflict: false },
  { lineNumber:31, content: '    this.greet();', isConflict: false },
  { lineNumber:32, content: '    this.logCount();', isConflict: true },
  { lineNumber:33, content: '  }', isConflict: false },
  { lineNumber:34, content: '};', isConflict: false },
  { lineNumber:35, content: '</script>', isConflict: false },
  { lineNumber:36, content: '', isConflict: false },
  { lineNumber:37, content: '<style scoped>', isConflict: false },
  { lineNumber:38, content: '.container {', isConflict: false },
  { lineNumber:39, content: '  padding: 40px;', isConflict: true, charConflictRanges: [{ start: 10, end: 12 }] },
  { lineNumber:40, content: '  background-color: #e0e0ff;', isConflict: true },
  { lineNumber:41, content: '}', isConflict: false },
  { lineNumber:42, content: '', isConflict: false },
  { lineNumber:43, content: 'h1 {', isConflict: false },
  { lineNumber:44, content: '  color: green;', isConflict: true },
  { lineNumber:45, content: '}', isConflict: false },
  { lineNumber:46, content: '', isConflict: false },
  { lineNumber:47, content: 'button {', isConflict: false },
  { lineNumber:48, content: '  background-color: lightgray;', isConflict: true },
  { lineNumber:49, content: '  border: 1px solid black;', isConflict: true },
  { lineNumber:50, content: '}', isConflict: false }
]
