-- Keep Markdown tables inside the publication text measure.
-- Pandoc's default longtable columns use natural widths; long Chinese cells can
-- therefore extend past the page edge in a publication proof. The weights are
-- intentionally modest and leave the table backend responsible for wrapping.
-- ctex suppresses ordinary spaces between Chinese words. Preserve deliberate
-- spaces in the author byline without changing paragraph whitespace handling.
function Meta(meta)
  if FORMAT ~= "latex" or not meta.author then return nil end
  local function preserve_spaces(value)
    if type(value) == "string" then
      return value:gsub(" ", "\u{00a0}")
    elseif pandoc.utils.type(value) == "Inlines" then
      return pandoc.walk_block(pandoc.Plain(value), {
        Space = function() return pandoc.Str("\u{00a0}") end
      }).content
    elseif pandoc.utils.type(value) == "List" then
      for i, author in ipairs(value) do value[i] = preserve_spaces(author) end
    end
    return value
  end
  meta.author = preserve_spaces(meta.author)
  return meta
end

function Table(tbl)
  local weights_by_column_count = {
    [2] = {0.34, 0.66},
    [3] = {0.22, 0.39, 0.39},
    [4] = {0.18, 0.25, 0.27, 0.30},
  }
  -- Respect widths already supplied by the author or a design filter.
  for _, colspec in ipairs(tbl.colspecs) do
    if type(colspec[2]) == "number" and colspec[2] > 0 then
      return tbl
    end
  end
  local weights = weights_by_column_count[#tbl.colspecs]
  if not weights then
    return tbl
  end
  for index, colspec in ipairs(tbl.colspecs) do
    tbl.colspecs[index] = {colspec[1], weights[index]}
  end
  return tbl
end

-- Expose list paragraphs to the reference document's pagination/spacing style.
-- Pandoc otherwise writes loose-list paragraphs without a named style.
function OrderedList(list)
  if FORMAT ~= "docx" then return nil end
  for _, item in ipairs(list.content) do
    for i, block in ipairs(item) do
      if block.t == "Plain" or block.t == "Para" then
        item[i] = pandoc.Div({pandoc.Para(block.content)},
          pandoc.Attr("", {}, {["custom-style"] = "List Paragraph"}))
      end
    end
  end
  return list
end

-- A supplied, numbered label immediately before a figure/table is its caption.
-- Put it into Pandoc's caption structure so each writer can keep it with its
-- object. This also replaces the implicit image-alt caption in Markdown input.
function Pandoc(doc)
  local blocks = pandoc.List()
  local i = 1
  while i <= #doc.blocks do
    local label, object = doc.blocks[i], doc.blocks[i + 1]
    local text = pandoc.utils.stringify(label)
    local is_label = label.t == "Para" and #label.content == 1
      and label.content[1].t == "Strong"
      and (text:match("^图%s*%d") or text:match("^表%s*%d")
        or text:match("^Figure%s+%d") or text:match("^Table%s+%d"))
    if is_label and object and object.t == "Table" then
      object.caption = {long = {label}}
      blocks:insert(object)
      i = i + 2
    elseif is_label and object and object.t == "Figure" then
      object.caption = {long = {label}}
      blocks:insert(object)
      i = i + 2
    elseif is_label and object and object.t == "Para"
      and #object.content == 1 and object.content[1].t == "Image" then
      blocks:insert(pandoc.Figure({object}, {long = {label}}))
      i = i + 2
    else
      blocks:insert(label)
      i = i + 1
    end
  end
  doc.blocks = blocks
  return doc
end
