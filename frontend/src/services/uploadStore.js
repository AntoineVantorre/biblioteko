let _file = null;
let _meta = {};

export function setUpload(file, meta = {}) {
  _file = file;
  _meta = meta;
}

export function getUpload() {
  return { file: _file, meta: _meta };
}

export function clearUpload() {
  _file = null;
  _meta = {};
}

export default { setUpload, getUpload, clearUpload };
